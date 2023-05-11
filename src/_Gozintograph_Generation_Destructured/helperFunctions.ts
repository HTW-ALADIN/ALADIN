const templateString = (template: string, valueObject: { [key: string]: string[] } = {}, concatWith: string = " ") => {
	let output = template;
	Object.entries(valueObject).forEach(([key, values]) => {
		output = output.replace(new RegExp("\\$" + `{${key}}`, "g"), () =>
			values.reduce((string, value, i) => (!i ? value : string + concatWith + value), "")
		);
	});
	return output;
};

const toPascalCase = (string: string) =>
	`${string}`
		.replace(/[-_]+/g, " ")
		.replace(/[^\w\s]/g, "")
		.replace(/\s+(.)(\w+)/g, ($1, $2, $3) => `${$2.toUpperCase() + $3.toLowerCase()}`)
		.replace(/\s/g, "")
		.replace(/\w/, (s) => s.toUpperCase());

const ensureType = (type: string, input: any): any | Array<any> => {
	const typeMap: { [key: string]: Function } = {
		string: (input: any) => input.toString(),
		int: (input: any) => parseInt(input),
		float: (input: any) => parseFloat(input),
	};
	if (Array.isArray(input)) {
		return input.map((i) => ensureType(type, i));
	}
	return typeMap[type](input);
};

export function* statefulCounter() {
	let i = 0;
	while (true) yield i++;
}

export { templateString, toPascalCase, ensureType };
