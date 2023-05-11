import { TaskGenerator } from "./TaskGenerator";
import { Constructor } from "./Utility";
import { Gozintograph, GozintographVertex } from "./Graph";
import { GozintographGenerator, GozintographConfig } from "./GraphGenerator";

export class GozintographTaskGenerator extends TaskGenerator<Gozintograph, GozintographConfig> {
	constructor(
		graphConstructor: Constructor<Gozintograph> = Gozintograph,
		generatorConstructor: Constructor<GozintographGenerator> = GozintographGenerator
	) {
		super(graphConstructor, generatorConstructor);
	}

	public generateTask(config: GozintographConfig) {
		config["type"] = "digraph";
		config["edgeDirection"] = "forward";
		config.style = {
			graph: { rankdir: "BT", splines: "polyline", bgcolor: "transparent" },
			vertex: { shape: "circle", style: "filled" },
			edge: {},
		};
		super.generateTask(config);

		const graphGenerator = new this.graphGeneratorConstructor(this.rng);
		this.graph = graphGenerator.generateGraph(this.graphConstructor, config);

		const transpose = (adjacencyMatrix: Array<Array<number>>) =>
			adjacencyMatrix[0].map((_, colIndex) => adjacencyMatrix.map((row) => row[colIndex]));
		const [labelVector, valueVector, adjacencyMatrix] = this.orderGraphSemantically(this.graph);
		// const vertices = Object.values(this.graph.getVertices());
		// const valueVector = vertices.map((vertex) => vertex.getProperty("value" as keyof GozintographVertex));
		// const labelVector = vertices.map((vertex) => vertex.getProperty("label" as keyof GozintographVertex));
		const solution = this.calculateSolution(transpose(adjacencyMatrix), valueVector);

		const dotGraph = this.graph.dotGraph();
		const { nodes, edges, paths } = this.graph.serialize();

		return {
			dotDescription: dotGraph,
			edges,
			nodes,
			paths,
			valueVector: [valueVector],
			labelVector,
			solution,
			adjacencyMatrix: transpose(adjacencyMatrix),
			longestPath: this.graph.getLongestPathLength(),
		};
	}

	private orderGraphSemantically(graph: Gozintograph) {
		const labelOrder: { [key: string]: number } = { P: 400, B: 300, K: 200, R: 100 };
		const vertices = Object.values(graph.getVertices());

		const labelSort = (v1: GozintographVertex, v2: GozintographVertex) => {
			const labels = [v1, v2].map((v) => v.getProperty("label" as keyof GozintographVertex));
			const splitAtIndex = (s: string, index: number): [label: string, index: number] => [
				s.substring(0, index),
				parseInt(s.substring(index)),
			];
			const [l1, l2] = labels.map((label) => splitAtIndex(label, 1));

			return labelOrder[l2[0]] - labelOrder[l1[0]] + (l1[1] - l2[1]);
		};
		const edges = graph.getEdges();

		return vertices.sort(labelSort).reduce(
			(sortedGraph, vertex, i, sortedVertices) => {
				sortedGraph[0].push(vertex.getProperty("label" as keyof GozintographVertex));
				sortedGraph[1].push(vertex.getProperty("value" as keyof GozintographVertex));

				const row = sortedVertices.map((sortedVertex) => {
					const parents = vertex.getParents();
					const vertexID = vertex.getId();
					const parentID = sortedVertex.getId();
					if (parentID in parents) {
						return parseInt(edges[`${parents[parentID].getId()}__${vertexID}`].getLabel());
					} else {
						return 0;
					}
				});
				sortedGraph[2].push(row);

				return sortedGraph;
			},
			[[], [], []]
		);
	}

	private longestPathLength() {
		const roots = this.graph.getLeafs();
		const vertices = this.graph.getVertices();
		const rootVertices = roots.map((root) => vertices[root]);

		const findPath = (vertex: GozintographVertex, path: Array<object>, paths: Array<Array<object>>) => {
			const childs = Object.values(vertex.getChilds());
			if (childs.length) {
				childs.forEach((child) => {
					let newPath = [...path];
					newPath.push({ between: [vertex.getId(), child.getId()] });
					findPath(child, newPath, paths);
				});
			} else if (path.length) {
				paths.push(path);
				path = [];
			}
			return paths;
		};

		const paths = rootVertices.reduce((paths, root) => findPath(root, [], paths), []);
		this.graph.setPaths(paths);

		const longestPathLength = paths.reduce(
			(longestPath, path) => (path.length > longestPath ? path.length : longestPath),
			0
		);

		this.graph.setLongestPathLength(longestPathLength);
		return longestPathLength;
	}

	private calculateSolution(matrix: Array<Array<number>>, valueVector: Array<number>): Array<Array<number>> {
		const transpose = (matrix: Array<Array<number>>) =>
			matrix[0].map((element, elementIndex) => matrix.map((row) => row[elementIndex]));
		const sum = (list: Array<number>): number => list.reduce((sum, element) => (sum += element), 0);
		const matmul = (m1: Array<Array<number>>, m2: Array<Array<number>>) =>
			m1.map((row) =>
				transpose(m2).map((column) => sum(row.map((element, elementIndex) => element * column[elementIndex])))
			);
		const matadd = (m1: Array<Array<number>>, m2: Array<Array<number>>) =>
			m1.map((row, i) => row.map((element, j) => (m2[i][j] += element)));
		const unity = (matrix: Array<Array<number>>) => {
			return matrix.reduce((unityMatrix, rows, i) => {
				const unityRow = rows.reduce((unityRow, row, j) => {
					unityRow[j] = i === j ? 1 : 0;
					return unityRow;
				}, []);
				unityMatrix.push(unityRow);
				return unityMatrix;
			}, [] as Array<Array<number>>);
		};

		let current = matrix;
		let result = matrix;
		const longestPathLength = this.longestPathLength();
		for (let i = 1; i < longestPathLength; i++) {
			result = matmul(current, result);
			result = matadd(current, result);
		}
		result = matadd(result, unity(matrix));

		const resultVector = result.reduce((vector, row) => {
			const scalar = row.reduce((scalar, element, i) => {
				scalar += element * valueVector[i];
				return scalar;
			}, 0);
			vector.push(scalar);
			return vector;
		}, [] as Array<number>);

		return [resultVector];
	}
}

// const tg = new GozintographTaskGenerator();
// const t = tg.generateTask({
//     nodeAmount: 10,
//     edgeDensity: 0.2,
//     nodeValueRange: [1, 10],
//     edgeWeightRange: [1, 10],
//     seed: "",
//     style: { vertex: {}, edge: {}, graph: {} },
// });
// console.log(t.paths);

// nodeAmount: number;
// edgeDensity: number;
// nodeValueRange: [number, number];
// edgeWeightRange: [number, number];
