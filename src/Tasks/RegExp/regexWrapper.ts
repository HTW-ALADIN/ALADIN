import { execSync } from 'child_process';
import { Console } from 'console';
import { array } from 'fp-ts';
import fs from 'fs';
import { spawn } from 'child_process';
import { exec } from 'child_process';
import { promisify } from 'util';

let rowCount = 0;
let columnCount = 0;
interface matrix extends Array<any>{}

interface RegexData  {
  columns: number;
  rows: number;
  seed: number;

}

function runPythonScript(scriptPath: string, args: string[]=[]): string {
  const command = `python ${scriptPath} ${args.join(' ')}`;
  try {
    const output = execSync(command, { encoding: 'utf-8' });
    return output.trim();
  } catch (error) {
    throw error.stderr.toString('utf-8');
  }
}

export function generateRegexPuzzle(regexData: RegexData) {
  try {

    const { columns, rows, seed } = regexData;
    const columnCount = columns;
    const rowCount = rows;
    const userseed = seed || Math.floor(Math.random() * 10000);

    const pythonScriptPath = 'src/Tasks/RegExp/regexFrontend.py';
    const argumentsToPythonScript = [columnCount.toString(), rowCount.toString(), userseed.toString()];
    runPythonScript(pythonScriptPath, argumentsToPythonScript);
    
    const f = fs.readFileSync('src/Tasks/RegExp/JSONFiles/labels.json', 'utf8')
    const {ColumnLabel, RowLabel} = JSON.parse(f);
  
    const Matrix: matrix = [];
    for (let i = 0; i < rowCount; i++) {
        const row: any[] = [];
        for (let j = 0; j < columnCount; j++) {
            row.push(null); 
        }
        Matrix.push(row);
    }
    return { ColumnLabel, RowLabel , Matrix};
  } catch (error) {
    console.error('Error running TS script:', error);
    throw error;
  }
}

const writeFileAsync = promisify(fs.writeFile);
const readFileAsync = promisify(fs.readFile);

export async function validateRegexPuzzle(validatonConfig: any) {
  try {
    const userData: matrix = validatonConfig.userData;
    const jsonData = JSON.stringify(userData, null, 2);

    await writeFileAsync('src/Tasks/RegExp/JSONFiles/userData.json', jsonData);
    
    const pythonScriptPath1 = 'src/Tasks/RegExp/validateRegex.py';
    await runPythonScript(pythonScriptPath1);

    const validationmatrixString = await readFileAsync('src/Tasks/RegExp/JSONFiles/validationmatrix.json', 'utf8');
    const validationmatrix: matrix = JSON.parse(validationmatrixString);
    
    return { validationmatrix };
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}


