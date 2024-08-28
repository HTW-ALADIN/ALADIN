import { GozintographTaskGenerator } from "../Legacy/Tasks/gozintograph/Task";
import { sqlQueryGenerator, sqlQueryValidator, importDatabase, fetchERD } from "../Legacy/Tasks/SQL/SQLTaskWorker";
import { semanticSqlQueryGenerator } from "../Legacy/Tasks/SQL/semanticSQLWorker/SQLTaskGenerator";
import { semanticSqlQueryValidator } from "../Legacy/Tasks/SQL/semanticSQLWorker/SQLValidator";
import { InterpolationTaskGenerator } from "../Legacy/Tasks/geoInterpolation/GeoInterpolationWorker";
import { ShortestPathTaskGenerator } from "../Legacy/Tasks/shortestPath/MunkeltWorker";
import { EPKTaskGenerator } from "../Legacy/Tasks/EPK/EPKTask";
import { SchedulingTaskGenerator } from "../Legacy/Tasks/scheduling/Task";
import { generateFermentationDataMain } from "../Tasks/Ferment/wrapperFunctionCallPython";

import fs from "fs";
import path from "path";

interface ISerializedQueues {
	[key: string]: {
		minConsumers: number;
		consumerInstructions: {
			[key: string]: {
				dependencies: Array<string>;
				body: string;
			};
		};
	};
}

interface SerializedTasks {
	[key: string]: { API: object; Worker: ISerializedQueues; UI: { [key: string]: object }; name: string };
}

function* yieldFilesFromDirectory(directory: string) {
	if (!fs.existsSync(directory)) {
		throw Error(`${directory}\nThis directory does not exist!`);
	}

	for (const filename of fs.readdirSync(directory)) {
		const filepath = path.resolve(directory, filename);
		yield { filename, file: fs.readFileSync(filepath, "utf8") };
	}
}

function readSerializedTasks(directory: string): SerializedTasks {
	const tasks: SerializedTasks = {};
	for (const { filename, file } of yieldFilesFromDirectory(directory)) {
		const name: string = path.parse(filename).name.toLowerCase();
		const task = JSON.parse(file);
		task["name"] = path.parse(filename).name;
		tasks[task.name] = task;
	}
	return tasks;
}

const AsyncFunction: any = Object.getPrototypeOf(async function () {}).constructor;

// TODO generalize generators into serialisable functions
const generators: { [key: string]: any } = {
	GozintographTaskGenerator: GozintographTaskGenerator,
	sqlQueryGenerator: sqlQueryGenerator,
	sqlQueryValidator: sqlQueryValidator,
	importDatabase: importDatabase,
	fetchERD: fetchERD,
	semanticSqlQueryGenerator: semanticSqlQueryGenerator,
	semanticSqlQueryValidator: semanticSqlQueryValidator,
	InterpolationTaskGenerator: InterpolationTaskGenerator,
	ShortestPathTaskGenerator: ShortestPathTaskGenerator,
	EPKTaskGenerator: EPKTaskGenerator,
	SchedulingTaskGenerator: SchedulingTaskGenerator,
	generateFermentationDataMain: generateFermentationDataMain,
};

export interface IInstructionConfiguration {
	type: string;
	instruction: string;
	parameters: { [key: string]: string | number | Array<any> | object };
}

// load environment variables
import * as dotenv from "dotenv";
dotenv.config({ path: __dirname + "/.env" });

const setupTasks = () => {
	try {
		const tasks = readSerializedTasks(`${__dirname}/tempTaskGraphStorage/tasks`);

		const taskParts = Object.entries(tasks).reduce(
			(taskParts, [name, task]) => {
				const api = task.API as Array<any>;
				taskParts.API = [...taskParts.API, ...api];
				taskParts.Worker = { ...taskParts.Worker, ...task.Worker };
				return taskParts;
			},
			{
				API: [],
				Worker: [],
			} as unknown as { API: any[]; Worker: ISerializedQueues }
		);

		// template and configure dockerfiles https://www.datanovia.com/en/courses/docker-compose-wait-for-dependencies/
		const queues: ISerializedQueues = taskParts.Worker;

		const taskWorkers: { [key: string]: any } = {};
		for (let queue in queues) {
			const queueConfig = queues[queue];
			// forbidden black magic:
			// https://stackoverflow.com/questions/36517173/how-to-store-a-javascript-function-in-json
			// https://stackoverflow.com/questions/6396046/unlimited-arguments-in-a-javascript-function
			const parsedFunctions = Object.entries(queueConfig.consumerInstructions).reduce(
				(parsedFunctions, [instructionName, instruction]) => {
					const parsedFunction: CallableFunction = new AsyncFunction(
						...instruction.dependencies.map((dependency) => generators[dependency].name),
						`"use strict"; return (${instruction.body});`
					)(...instruction.dependencies.map((dependency) => generators[dependency]));
					return { ...parsedFunctions, [instructionName]: parsedFunction };
				},
				{} as { [key: string]: CallableFunction }
			);
			taskWorkers[queue] = parsedFunctions;
		}

		return taskWorkers;
	} catch (error) {
		console.log(error);
	}
};

const taskWorkers = setupTasks();

export const executeTask = async (instructionConfiguration: IInstructionConfiguration) => {
	// const { instruction } = instructionConfiguration;
	// return await parsedFunctions[instruction](instructionConfiguration);
	try {
		const { type, instruction } = instructionConfiguration;
		const func = await taskWorkers[`${type}Task`][instruction];
		const result = await func(instructionConfiguration);
		return result;
	} catch (error) {
		console.log(error);
	}
};
