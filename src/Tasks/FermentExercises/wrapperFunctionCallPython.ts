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
	let frontendEingaben: any;
	if (parameter === undefined || parameter === null) {
		throw new Error("Parameter ist undefined oder null.");
	}
	if (typeof parameter === "string") {
		try {
			frontendEingaben = JSON.parse(parameter);
		} catch (error) {
			throw new Error("Fehler beim Parsen des JSON-Strings: " + error.message);
		}
	} else if (typeof parameter === "object") {
		frontendEingaben = parameter;
	} else {
		throw new Error("Ungültiges Eingabeformat für parameter.");
	}
	return frontendEingaben;
}
function cleanAndMoveParameters(frontendEingaben : any) {
	if (frontendEingaben && frontendEingaben.parameters) {
		// Inhalt von "parameters" ins Hauptobjekt verschieben
		Object.assign(frontendEingaben, frontendEingaben.parameters);

		// Entfernen der spezifizierten Schlüssel
		delete frontendEingaben.parameters;
		delete frontendEingaben.type;
		delete frontendEingaben.task;
		delete frontendEingaben.Paramter; 
		delete frontendEingaben.instruction;
		delete frontendEingaben.language;
	}

	return frontendEingaben;
}

// Schlüsselnamen im Objekt ändern
function  renameKey (obj: any, oldKey: string, newKey: string) {
	if (obj.hasOwnProperty(oldKey)) {
		obj[newKey] = obj[oldKey];
		delete obj[oldKey];
	}
	for (const key in obj) {
		if (obj.hasOwnProperty(key) && typeof obj[key] === "object" && obj[key] !== null) {
			renameKey(obj[key], oldKey, newKey);
		}
	}
	return obj;
};

function editSaveParams(parameter: any) {
	//Überprüfen, ob parameter ein String ist und wenn ja, ihn parsen
	let frontendEingaben : any = parseFrontendInputs(parameter);
	frontendEingaben = cleanAndMoveParameters(frontendEingaben);

	frontendEingaben =  renameKey(frontendEingaben, "nodeAmount", "Modell");
	frontendEingaben = renameKey(frontendEingaben, "seed", "PhasenAnzahl");

	//Modell-Schlüssel umbennen
	switch (frontendEingaben.Modell) {
		case "S.cerevisiae":
			frontendEingaben.Modell = "Modell-1";
			break;
		case "E.coli":
			frontendEingaben.Modell = "Modell-2";
			break;
		case "Testorganismus":
			frontendEingaben.Modell = "Modell-3";
			break;
	}
	let phasenanzahl = parseInt(frontendEingaben.PhasenAnzahl);
	frontendEingaben.PhasenAnzahl = phasenanzahl;
	
	let zuluft = [];
	let feed = [];
	let drehzahl = [];
	let druck = [];
	let dauer = [];
	let bolusC = [];
	let bolusN = [];
	for (let i = 0; i < phasenanzahl; i++) {
		if (Array.isArray(frontendEingaben.userDataMatrix[i][0])) {
			zuluft[i] = isNaN(parseFloat(frontendEingaben.userDataMatrix[i][0][0]))
				? 0
				: parseFloat(frontendEingaben.userDataMatrix[i][0][0]);
			feed[i] = isNaN(parseFloat(frontendEingaben.userDataMatrix[i][2][0]))
				? 0
				: parseFloat(frontendEingaben.userDataMatrix[i][2][0]);
			drehzahl[i] = isNaN(parseFloat(frontendEingaben.userDataMatrix[i][4][0]))
				? 0
				: parseFloat(frontendEingaben.userDataMatrix[i][4][0]);
			druck[i] = isNaN(parseFloat(frontendEingaben.userDataMatrix[i][5][0]))
				? 0
				: parseFloat(frontendEingaben.userDataMatrix[i][5][0]);
			dauer[i] = isNaN(parseFloat(frontendEingaben.userDataMatrix[i][6][0]))
				? 0
				: parseFloat(frontendEingaben.userDataMatrix[i][6][0]);
			bolusC[i] = isNaN(parseFloat(frontendEingaben.userDataMatrix[i][1][0]))
				? 0
				: parseFloat(frontendEingaben.userDataMatrix[i][1][0]);
			bolusN[i] = isNaN(parseFloat(frontendEingaben.userDataMatrix[i][3][0]))
				? 0
				: parseFloat(frontendEingaben.userDataMatrix[i][3][0]);
		} else {
			zuluft[i] = isNaN(parseFloat(frontendEingaben.userDataMatrix[i][0]))
				? 0
				: parseFloat(frontendEingaben.userDataMatrix[i][0]);
			feed[i] = isNaN(parseFloat(frontendEingaben.userDataMatrix[i][2]))
				? 0
				: parseFloat(frontendEingaben.userDataMatrix[i][2]);
			drehzahl[i] = isNaN(parseFloat(frontendEingaben.userDataMatrix[i][4]))
				? 0
				: parseFloat(frontendEingaben.userDataMatrix[i][4]);
			druck[i] = isNaN(parseFloat(frontendEingaben.userDataMatrix[i][5]))
				? 0
				: parseFloat(frontendEingaben.userDataMatrix[i][5]);
			dauer[i] = isNaN(parseFloat(frontendEingaben.userDataMatrix[i][6]))
				? 0
				: parseFloat(frontendEingaben.userDataMatrix[i][6]);
			bolusC[i] = isNaN(parseFloat(frontendEingaben.userDataMatrix[i][1]))
				? 0
				: parseFloat(frontendEingaben.userDataMatrix[i][1]);
			bolusN[i] = isNaN(parseFloat(frontendEingaben.userDataMatrix[i][3]))
				? 0
				: parseFloat(frontendEingaben.userDataMatrix[i][3]);
		}
	}

	delete frontendEingaben.userDataMatrix;

	frontendEingaben.Dauer = dauer;
	frontendEingaben.Druck = druck;
	frontendEingaben.Drehzahl = drehzahl;
	frontendEingaben.Zuluft = zuluft;
	frontendEingaben.BolusC = bolusC;
	frontendEingaben.Feed = feed;
	frontendEingaben.BolusN = bolusN;

	frontendEingaben.temperatur =isNaN(parseFloat(frontendEingaben.Temperatur)) ? 0 : parseFloat(frontendEingaben.Temperatur);
	frontendEingaben.startbiomasse = isNaN(parseFloat(frontendEingaben.BTM)) ? 0 : parseFloat(frontendEingaben.BTM);
	frontendEingaben.do = isNaN(parseFloat(frontendEingaben.DO)) ? 0 : parseFloat(frontendEingaben.DO)  ;
	delete frontendEingaben.Temperatur;
	delete frontendEingaben.BTM;
	delete frontendEingaben.DO;

	let dataTmp:any = frontendEingaben.maxParameter;
	delete frontendEingaben.maxParameter;
	frontendEingaben.maxParameter = dataTmp;
	dataTmp = frontendEingaben.minParameter;
	delete frontendEingaben.minParameter;
	frontendEingaben.minParameter=dataTmp;
	dataTmp = frontendEingaben.varierendeParameter;
	delete frontendEingaben.varierendeParameter;
	frontendEingaben.varierendeParameter=dataTmp;

	/*
	let maxParameter: string = '';
	let minParameter: string = '';
	let varierendeParameter :  object =  {};
	maxParameter = frontendEingaben.maxParameter;
	minParameter  = frontendEingaben.minParameter;
	varierendeParameter  = frontendEingaben.varierendeParameter;*/

	delete frontendEingaben.userDataInputFelder;
	delete frontendEingaben.checkUserDataValidity;



	// Pfad zur JSON-Datei definieren
	const filePfade = path.join(__dirname, "/interne_daten/FrontendEingaben.json");

	// JSON.stringify mit einer Replacer-Funktion
	let jsonString = JSON.stringify(frontendEingaben, null, 4);

	// Datei schreiben
	try {
		fs.writeFileSync(filePfade, jsonString, "utf-8");
		return true;
	} catch (error) {
		return false;
	}


	
}

export async function generateFermentExercises(parameter: any) {
	let check = editSaveParams(parameter)
	if (check) {
		let result = { foo: "bar" };
		try {
			let pythonScriptPath = "generateFermentExercises.py";
			pythonScriptPath = path.join(__dirname, pythonScriptPath);
			(await runPythonScript(pythonScriptPath)) as any;

			result = JSON.parse(fs.readFileSync(path.join(__dirname, "data.json"), "utf-8"));
			const filePath = path.join(__dirname, "data.json");
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