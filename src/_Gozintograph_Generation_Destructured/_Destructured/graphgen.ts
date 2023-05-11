enum ComputingEnvironment {
	Typescript = 0,
	Docker = 1,
	Python = 2,
	Javascript = 3,
	Java = 4,
	"C++" = 5,
}

class ComputationalWorkflowNode {
	constructor(private computingEnvironment: ComputingEnvironment) {}
}

enum PrimitiveTypes {
	any,
	string,
	int,
	float,
	bool,
}

enum CollectionTypes {
	array,
	map,
	set,
}

type TypedVertexCollectionType = {
	[collectionType in CollectionTypes]: PrimitiveTypes;
};

interface VertexAttributeMap {
	[key: string]: PrimitiveTypes | TypedVertexCollectionType;
}

class VertexFactory {
	constructor(vertexTypeName: string, vertexAttributes: VertexAttributeMap) {}
}

class DiGraph {
	private static counter: number = 0;
	private id: number = 0;

	constructor(nodeTypes: Array<typeof VertexFactory>) {
		DiGraph.counter++;
	}

	public addNode() {}
	public removeNode() {}

	public addEdge() {}
	public removeEdge() {}
}

export type Graphs = "";

export type NodeID = string;
export type EdgeID = string;

export interface Node {
	id: string;
	neighbours: Array<Node>;
}
export interface DiEdge {
	id: EdgeID;
	from: NodeID;
	to: NodeID;
}
