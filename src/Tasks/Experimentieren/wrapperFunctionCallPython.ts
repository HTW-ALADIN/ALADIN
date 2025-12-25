import fs from "fs";
const path = require("path");

function saveFrontendUserData(userDataObject: Record<string, any>) : boolean{
	const filePath = path.join(__dirname, "/internData/frontendUserData.json");
    
	let jsonString = JSON.stringify(userDataObject, null, 4);
	
	try {
		fs.writeFileSync(filePath, jsonString, "utf-8");
		return true;
	} catch (error) {
		return false;
	}
}


export function generateExperimentierenDataMain(userDataObject: any) {
    const check = saveFrontendUserData(userDataObject);
    return check;
}