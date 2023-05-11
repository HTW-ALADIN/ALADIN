import { Vertex, Edge, Graph, VertexParameters, EdgeParameters, GraphParameters } from "./genericGraphs/Graph";
import { Constructor, mapAttributesToDot } from "./Utility";

export interface PlanVertexParameters extends VertexParameters {}
export class GozintographVertex extends Vertex {
	private value: string;
	private label: string;
	constructor(args: PlanVertexParameters) {
		super(args);
		this.value = args.value;
		this.label = args.label;
	}

	public getProperty(property: keyof GozintographVertex): any {
		return this[property];
	}
	public setProperty(property: keyof GozintographVertex, value: any) {
		this[property] = value;
	}
	public getChilds(): { [id: number]: GozintographVertex } {
		return this.childs as { [id: number]: GozintographVertex };
	}
	public getParents(): { [id: number]: GozintographVertex } {
		return this.parents as { [id: number]: GozintographVertex };
	}
	public dotVertex() {
		return `${this.id} [label="${this.label}" tooltip="${this.value}"]`;
	}
	public serialize() {
		return {
			id: this.id,
			label: this.label,
			value: this.value,
			parents: Object.keys(this.parents),
			childs: Object.keys(this.childs),
		};
	}
}

export class GozintographEdge extends Edge {
	public dotEdge() {
		const weight = this.label;
		const parentId = this.parentVertices[0].getId();
		const childId = this.childVertices[0].getId();
		return `${parentId} -> ${childId} [label="${weight}"]`;
	}

	public serialize() {
		const [from, to] = this.id.split("__");
		return { between: [from, to], weight: this.label };
	}
}

interface GozintographParameters extends GraphParameters {}
export class Gozintograph extends Graph<GozintographVertex, GozintographEdge> {
	private adjacencyMatrix: Array<Array<number>>;
	private roots: Array<number>;
	private leafs: Array<number>;
	private paths: Array<Array<GozintographVertex>>;
	private longestPathLength: number;
	constructor(
		args: GozintographParameters,
		vertexConstructor: Constructor<GozintographVertex> = GozintographVertex,
		edgeConstructor: Constructor<GozintographEdge> = GozintographEdge
	) {
		super(args, vertexConstructor, edgeConstructor);
	}

	public getAdjacencyMatrix() {
		return this.adjacencyMatrix;
	}
	public setAdjacencyMatrix(adjacencyMatrix: Array<Array<number>>) {
		this.adjacencyMatrix = adjacencyMatrix;
	}
	public getRoots() {
		return this.roots;
	}
	public setRoots(roots: Array<number>) {
		this.roots = roots;
	}
	public getLeafs() {
		return this.leafs;
	}
	public setLeafs(leafs: Array<number>) {
		this.leafs = leafs;
	}
	public getPaths() {
		return this.paths;
	}
	public setPaths(paths: Array<Array<GozintographVertex>>) {
		this.paths = paths;
	}
	public getLongestPathLength() {
		return this.longestPathLength;
	}
	public setLongestPathLength(longestPathLength: number) {
		this.longestPathLength = longestPathLength;
	}

	public dotGraph() {
		const rankString = `{ rank=max; ${this.roots.join(";")} }\n }`;
		return super.dotGraph().replace("}", rankString);
	}
	public serialize() {
		const edges = Object.values(this.edges).map((edge) => edge.serialize());
		const vertices = Object.values(this.vertices).map((vertex) => vertex.serialize());
		return { nodes: vertices, edges, paths: this.paths };
	}
}
