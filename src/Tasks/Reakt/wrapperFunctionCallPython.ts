import { exec } from "child_process";
import fs from "fs";
const path = require("path");

function runPythonScript(scriptPath: string): Promise<string> {
	try {
		return new Promise((resolve, reject) => {
			const command = `python ${scriptPath}`;
			console.log(command);
			exec(command, (error, stdout, stderr) => {
				if (error) {
					reject(error.message);
					return;
				}
				if (stderr) {
					reject(stderr);
					return;
				}
				resolve(stdout);
			});
		});
	} catch {
		console.log("Error");
	}
}

function parseFrontendInputs(parameter: any) {
	//Überprüfen, ob parameter ein String ist und wenn ja, ihn parsen
	let frontendData: any;
	if (parameter === undefined || parameter === null) {
		throw new Error("Parameter ist undefined oder null.");
	}
	if (typeof parameter === "string") {
		try {
			frontendData = JSON.parse(parameter);
		} catch (error) {
			throw new Error("Fehler beim Parsen des JSON-Strings: " + error.message);
		}
	} else if (typeof parameter === "object") {
		frontendData = parameter;
	} else {
		throw new Error("Ungültiges Eingabeformat für parameter.");
	}
	return frontendData;
}
function cleanAndMoveParameters(frontendData : any) {
	if (frontendData && frontendData.parameters) {
		// Inhalt von "parameters" ins Hauptobjekt verschieben
		Object.assign(frontendData, frontendData.parameters);

		// Entfernen der spezifizierten Schlüssel
		delete frontendData.parameters;
		delete frontendData.type;
		delete frontendData.task;
		delete frontendData.Paramter; 
		delete frontendData.instruction;
		delete frontendData.language;
	}

	return frontendData;
}

function setColumnLabels(frontendData : any){
	let matrixData	=	frontendData['matrixData'];
	

	let vH2O2_AS_tmpArray	=	[];
	let cH2O2_AS_tmpArray	=	[];
	let v_Start_tmpArray	=	[];
	let t_Start_tmpArray	=	[];

	for( let i=0 ; i < matrixData.length ; i++){
		vH2O2_AS_tmpArray[i]	=	matrixData[i][0];
		cH2O2_AS_tmpArray[i]	=	matrixData[i][1];
		v_Start_tmpArray[i]		=	matrixData[i][2];
		t_Start_tmpArray[i]		=	matrixData[i][3];
	}
	
	let tmpArray : Object	=	{
		'VH2O2_AS' 	:	vH2O2_AS_tmpArray,
		'CH2O2_AS'	:	cH2O2_AS_tmpArray,
		'V_Start'	:	v_Start_tmpArray,
		'T_Start'	:	t_Start_tmpArray
	};
	

	frontendData['matrixData'] = tmpArray;
	return frontendData;
}

function SaveUserInputs(parameter: any) {
	//Überprüfen, ob parameter ein String ist und wenn ja, ihn parsen
	let frontendData : any = parseFrontendInputs(parameter);
	frontendData = cleanAndMoveParameters(frontendData);
	frontendData = setColumnLabels(frontendData);
	// Pfad zur JSON-Datei definieren
	const filePfade = path.join(__dirname, "/interneDaten/FrontendEingaben.json");

	// JSON.stringify mit einer Replacer-Funktion
	let jsonString = JSON.stringify(frontendData, null, 4);

	// Datei schreiben
	try {
		fs.writeFileSync(filePfade, jsonString, "utf-8");
		return true;
	} catch (error) {
		return false;
	}
}

export async function generateReactionData(parameter: any) {
	SaveUserInputs(parameter);
	if (true) {
		let result = { foo: "bar" };
		try {
			let pythonScriptPath = "generateReactionData.py";
			pythonScriptPath = path.join(__dirname, pythonScriptPath);
			(await runPythonScript(pythonScriptPath)) as any;

			result = JSON.parse(fs.readFileSync(path.join(__dirname, "Reaktdata.json"), "utf-8"));
			const filePath = path.join(__dirname, "Reaktdata.json");
			fs.writeFileSync(filePath, JSON.stringify(result, null, 2), "utf-8");
			
			//console.log(result);
			//insofern kryptsiche Zeichen in der JSON Ausgabe vorhanden sind .> Workaround mittels File
		} catch (error) {
			console.error("Error running Python script:", error);
		}
		return result;
	} else console.error("Die Daten aus Frontend konnten nicht in JSON-Datei gespeichert");
	return null;
}