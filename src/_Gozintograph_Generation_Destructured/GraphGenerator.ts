import { Gozintograph, GozintographVertex } from "./Graph";
import { GraphGenerator } from "./GraphGeneration";
import { Constructor, flatten } from "./Utility";
import { TaskConfig } from "./TaskGenerator";
import { ensureType, statefulCounter } from "./helperFunctions";

export interface GozintographConfig extends TaskConfig {
	nodeAmount: number;
	edgeDensity: number;
	nodeValueRange: [number, number];
	edgeWeightRange: [number, number];
}

export class GozintographGenerator extends GraphGenerator<Gozintograph, GozintographConfig> {
	public generateGraph(graphConstructor: Constructor<Gozintograph>, config: GozintographConfig) {
		GozintographVertex.resetCounter();
		config.type = "digraph";
		const graph = super.generateGraph(graphConstructor, config);

		const nodeAmount = ensureType("int", config.nodeAmount);
		const edgeDensity = ensureType("float", config.edgeDensity);
		const edgeWeightRange = config.edgeWeightRange.map((value) => ensureType("int", value)) as [number, number];
		const nodeValueRange = config.nodeValueRange.map((value) => ensureType("int", value)) as [number, number];

		const adjacencyMatrix = this.generateAdjacencyMatrix(edgeDensity, nodeAmount, edgeWeightRange);
		this.graph.setAdjacencyMatrix(adjacencyMatrix);
		this.buildGraph(adjacencyMatrix, nodeValueRange);

		return graph;
	}

	private generateAdjacencyMatrix(edgeDensity: number, nodeAmount: number, edgeWeightRange: [number, number]) {
		const randomDAG = (x: number, n: number) => {
			const length = (n * (n - 1)) / 2;
			const dag = new Array(length).fill(1);
			for (let i = 0; i < length; i++) {
				if (this.rng.floatBetween(0, 1) > x) {
					dag[i] = 0;
					if (!isConnected(n, dag)) dag[i] = 1;
				}
			}
			return dag;
		};

		const dagIndex = (n: number, i: number, j: number) => n * i + j - ((i + 1) * (i + 2)) / 2;

		const isConnected = (n: number, dag: Array<number>) => {
			const reached = new Array(n).fill(false);
			reached[0] = true;
			const queue = [0];

			while (queue.length > 0) {
				const x = queue.shift();
				for (let i = 0; i < n; i++) {
					if (i !== n && !reached[i]) {
						const j = i < x ? dagIndex(n, i, x) : dagIndex(n, x, i);
						if (dag[j] !== 0) {
							reached[i] = true;
							queue.push(i);
						}
					}
				}
			}
			return reached.every((x) => x);
		};

		const dagToAdjacencyMatrix = (n: number, dag: Array<number>, edgeWeightRange: [number, number]) => {
			const [min, max] = edgeWeightRange;
			let adjacencyMatrix = Array(n)
				.fill(null)
				.map(() => Array(n).fill(0));
			for (let i = 0; i < n; i++) {
				for (let j = i + 1; j < n; j++) {
					const k = dagIndex(n, i, j);

					if (dag[k]) adjacencyMatrix[j][i] = this.rng.intBetween(min, max);
				}
			}
			return adjacencyMatrix;
		};

		return dagToAdjacencyMatrix(nodeAmount, randomDAG(edgeDensity, nodeAmount), edgeWeightRange);
	}

	private buildGraph(adjacencyMatrix: Array<Array<number>>, nodeValueRange: [number, number]) {
		const rootVertices = this.findRoots(adjacencyMatrix);
		const leafVertices = this.findLeafs(adjacencyMatrix);
		this.graph.setLeafs(leafVertices);
		this.graph.setRoots(rootVertices);
		const [min, max] = nodeValueRange;
		const labels: { [key: string]: any } = {
			P: statefulCounter(),
			B: statefulCounter(),
			K: statefulCounter(),
			R: statefulCounter(),
		};
		adjacencyMatrix.forEach((row, i) => {
			const labelType = this.assignLabel(rootVertices, leafVertices, i);
			const vertex = this.graph.createVertex({
				value: this.rng.intBetween(min, max),
				label: `${labelType}${labels[labelType].next().value}`,
			});
			row.forEach((neighbour, j) => {
				if (neighbour) {
					const vertices = this.graph.getVertices();
					const parent = vertices[j];
					this.graph.createEdge({ parentVertices: [parent], childVertices: [vertex], label: neighbour.toString() });
				}
			});
		});
	}

	private assignLabel(rootVertices: Array<number>, leafVertices: Array<number>, i: number) {
		let labelType = "B";
		if (leafVertices.includes(i)) labelType = this.rng.coinFlip() ? "R" : "K";
		else if (rootVertices.includes(i)) labelType = "P";

		return labelType;
	}

	private findRoots(adjacencyMatrix: Array<Array<number>>) {
		const transpose = (adjacencyMatrix: Array<Array<number>>) =>
			adjacencyMatrix[0].map((_, colIndex) => adjacencyMatrix.map((row) => row[colIndex]));

		return this.findLeafs(transpose(adjacencyMatrix));
	}
	private findLeafs(adjacencyMatrix: Array<Array<number>>) {
		return adjacencyMatrix
			.map((vertex, i) => (vertex.every((weight) => !weight) ? i : -1))
			.filter((isLeaf) => isLeaf !== -1);
	}
}
