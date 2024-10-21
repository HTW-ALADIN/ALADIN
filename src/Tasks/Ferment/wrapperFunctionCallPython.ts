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
function parameterBearbeitenUndSpeichern(parameter: any) {
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

	// Einige Schlüsseln Schlüssel entfernen und dessen Inhalt verschieben
	if (frontendEingaben && frontendEingaben.parameters) {
		// Inhalt von "parameters" ins Hauptobjekt verschieben
		Object.assign(frontendEingaben, frontendEingaben.parameters);
		// Schlüsseln entfernen
		delete frontendEingaben.parameters;
		delete frontendEingaben.type;
		delete frontendEingaben.task;
		delete frontendEingaben.instruction;
		delete frontendEingaben.language;
	}

	// Schlüsselnamen im Objekt ändern
	const renameKey = (obj: any, oldKey: string, newKey: string) => {
		if (obj.hasOwnProperty(oldKey)) {
			obj[newKey] = obj[oldKey];
			delete obj[oldKey];
		}
		for (const key in obj) {
			if (obj.hasOwnProperty(key) && typeof obj[key] === "object" && obj[key] !== null) {
				renameKey(obj[key], oldKey, newKey);
			}
		}
	};
	renameKey(frontendEingaben, "nodeAmount", "Modell");
	renameKey(frontendEingaben, "seed", "PhasenAnzahl");

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

	let temperatur: number = 0;
	let dO: number = 0;
	let startbiomasse: number = 0;
	if (frontendEingaben.userDataInputFelder) {
		temperatur = parseFloat(frontendEingaben.userDataInputFelder.T);
		dO = parseFloat(frontendEingaben.userDataInputFelder.DO);
		startbiomasse = parseFloat(frontendEingaben.userDataInputFelder.BTM);

		delete frontendEingaben.userDataInputFelder;
	}
	frontendEingaben.temperatur = isNaN(temperatur) ? 0 : temperatur;
	frontendEingaben.startbiomasse = isNaN(startbiomasse) ? 0 : startbiomasse;
	frontendEingaben.do = isNaN(dO) ? 0 : dO;

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

export async function generateFermentationDataMain(parameter: any) {
	let check = parameterBearbeitenUndSpeichern(parameter);
	if (check) {
		let result = { foo: "bar" };
		try {
			let pythonScriptPath = "generateFermentationData.py";
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
