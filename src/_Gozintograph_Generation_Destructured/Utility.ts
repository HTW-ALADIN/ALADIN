export type Constructor<T> = { new (...args: Array<any>): T };

export const mapAttributesToDot = (attributes: object) =>
	Object.entries(attributes)
		.map(([key, value]) => `${key}="${value}"`)
		.join(" ");

export const flatten = (a: Array<any>, depth: number = 1) => {
	const result = [];
	const stack = [...a.map((item) => [item, depth])];

	while (stack.length > 0) {
		const [top, depth] = stack.pop();
		if (Array.isArray(top) && depth > 0) {
			stack.push(...top.map((item) => [item, depth - 1]));
		} else {
			result.push(top);
		}
	}

	return result.reverse();
};
