import { Observable, Observer, ObservableEvent } from "../Observer";
import { NodeShapes, GraphStyle, EdgeStyle, NodeStyle } from "../GraphViz";
import { Constructor, mapAttributesToDot } from "../Utility";

export interface VertexParameters {
	shape?: keyof typeof NodeShapes;
	style?: { [key: string]: string };
	[key: string]: any;
}
export class Vertex {
	static counter = 0;
	protected id: number;
	protected parents: { [id: number]: Vertex } = {};
	protected childs: { [id: number]: Vertex } = {};
	protected shape: string;
	protected style: VertexParameters["style"];

	constructor(args: VertexParameters) {
		const { shape, style } = args;
		this.id = Vertex.counter++;
		this.shape = shape || "";
		this.style = style || {};
	}

	static resetCounter() {
		Vertex.counter = 0;
	}
	public getId(): number {
		return this.id;
	}
	public addParents(parents: { [id: number]: Vertex }) {
		this.parents = { ...this.parents, ...parents };
	}
	public addChilds(childs: { [id: number]: Vertex }) {
		this.childs = { ...this.childs, ...childs };
	}
	public removeParent(parent: number) {
		delete this.parents[parent];
	}
	public removeChild(child: number) {
		delete this.parents[child];
	}
	public getParents() {
		return this.parents;
	}
	public getChilds() {
		return this.childs || {};
	}
	public dotVertex(style: VertexParameters["style"] = null, ...args: Array<any>): string {
		style = style || this.style;
		const vertexAttributes = mapAttributesToDot(style);
		return `${this.id} [ shape="${this.shape}" label="${this.id}" tooltip="${this.id}", ${vertexAttributes}]`;
	}
	public serialize() {
		return { id: this.id, parents: Object.keys(this.parents), childs: Object.keys(this.childs) };
	}
}

export interface EdgeParameters {
	parentVertices: { [id: number]: Vertex };
	childVertices: { [id: number]: Vertex };
	style?: { [key: string]: string };
	label?: string;
	shape?: string;
}
export class Edge {
	protected id: string;
	protected label: string;
	protected shape: string;
	protected style: EdgeParameters["style"];
	protected parentVertices: { [id: number]: Vertex };
	protected childVertices: { [id: number]: Vertex };

	constructor(args: EdgeParameters) {
		const { parentVertices, childVertices, label, shape, style } = args;
		this.label = label || "";
		this.shape = shape || "";
		this.style = style || {};
		this.parentVertices = parentVertices;
		this.childVertices = childVertices;
		const parentIds = Object.values(parentVertices)
			.map((vertex) => vertex.getId())
			.join("_");
		const childIds = Object.values(childVertices)
			.map((vertex) => vertex.getId())
			.join("_");
		this.id = `${parentIds}__${childIds}`;

		Object.values(childVertices).forEach((child) =>
			Object.values(parentVertices).forEach((parent) => {
				child.addParents({ [parent.getId()]: parent });
				parent.addChilds({ [child.getId()]: child });
			})
		);
	}

	public getId() {
		return this.id;
	}
	public getLabel() {
		return this.label;
	}
	public getParentVertices() {
		return this.parentVertices;
	}
	public getChildVertices() {
		return this.childVertices;
	}
	/**
	 * @returns concatenated edge-strings to make hyperedges possible in the dot language if multiple parents or childs
	 * @returns one edge-string if one parent and one child
	 */
	public dotEdge(style: EdgeParameters["style"] = null, ...args: Array<any>): string {
		style = style || this.style;
		const edgeAttributes = mapAttributesToDot(style);
		return Object.keys(this.parentVertices).reduce((hyperEdge, parentId) => {
			const edgeStrings = Object.keys(this.childVertices)
				.map((childId) => `${this.shape} ${parentId} -> ${childId} [${edgeAttributes}]`)
				.join("\n");
			return `${hyperEdge}\n ${edgeStrings}`;
		}, "");
	}

	public serialize(): any {
		const [from, to] = this.id.split("__");
		return { from, to, label: this.label };
	}
}

export interface GraphEvent extends ObservableEvent {
	type: "vertexInsertion" | "vertexRemoval" | "edgeInsertion" | "edgeRemoval";
	data: {
		id: Vertex["id"] | Edge["id"];
		graph: Graph<Vertex, Edge>;
	};
}
export interface GraphParameters {
	style: {
		graph: GraphStyle;
		vertex: NodeStyle;
		edge: EdgeStyle;
	};
	type?: "graph" | "digraph";
	edgeDirection?: "forward" | "backward";
	seed?: string;
}
/**
 * Observable Graph BaseClass
 */
export abstract class Graph<V extends Vertex, E extends Edge> implements Observable {
	private observers: Array<Observer> = [];

	protected vertices: { [id: number]: V } = {};
	protected edges: { [id: string]: E } = {};
	protected type: GraphParameters["type"];
	protected edgeDirection: GraphParameters["edgeDirection"];
	protected style: GraphParameters["style"];
	constructor(
		args: GraphParameters,
		protected vertexConstructor: Constructor<V> = vertexConstructor,
		protected edgeConstructor: Constructor<E> = edgeConstructor
	) {
		const { type, style } = args;
		this.type = type;
		this.style = style;
		this.edgeDirection = args.edgeDirection;
	}

	public createVertex<P extends VertexParameters>(args: P): V {
		const vertex = new this.vertexConstructor(args);
		this.vertices = { ...this.vertices, [vertex.getId()]: vertex };
		this.notify({ type: "vertexInsertion", data: { id: vertex.getId(), graph: this } });
		return vertex;
	}
	public createEdge<P extends EdgeParameters>(args: P): E {
		const edge = new this.edgeConstructor(args);
		this.edges = { ...this.edges, [edge.getId()]: edge };
		this.notify({ type: "edgeInsertion", data: { id: edge.getId(), graph: this } });
		return edge;
	}
	public removeVertex(id: number) {
		delete this.vertices[id];
	}
	public removeEdge(id: string) {
		delete this.edges[id];
		const [parentId, childId] = id.split("__").map((id) => parseInt(id));
		this.vertices[parentId].removeChild(childId);
		this.vertices[childId].removeChild(parentId);
	}
	public getVertex(id: number): V {
		return this.vertices[id];
	}
	public getEdge(id: string): E {
		return this.edges[id];
	}
	public getEdges() {
		return this.edges;
	}
	public getVertices() {
		return this.vertices;
	}

	public dotGraph(...args: Array<any>): string {
		const graphAttributes = mapAttributesToDot(this.style.graph);
		const vertexAttributes = mapAttributesToDot(this.style.vertex);
		const edgeAttributes = mapAttributesToDot(this.style.edge);
		const graphStyle = `graph [bgcolor="transparent" ${graphAttributes}]`;
		const vertexStyle = `node [${vertexAttributes}] `;
		const edgeStyle = `edge [${edgeAttributes}] `;
		const vertexString = Object.values(this.vertices)
			.map((vertex) => vertex.dotVertex())
			.join("\n");
		const edgeString = Object.values(this.edges)
			.map((edge) => edge.dotEdge())
			.join("\n");

		return `${this.type} {
            ${graphStyle}
            ${vertexStyle}
            ${vertexString}
            ${edgeStyle}
            ${edgeString}
        }`;
	}

	public serialize() {
		const edges = Object.values(this.edges).map((edge) => edge.serialize());
		const vertices = Object.values(this.vertices).map((vertex) => vertex.serialize());
		return { nodes: vertices, edges };
	}

	public attach(observer: Observer): void {
		if (this.observers.includes(observer)) return;
		this.observers.push(observer);
	}

	public detach(observer: Observer): void {
		const observerIndex = this.observers.indexOf(observer);
		if (observerIndex !== -1) {
			this.observers.splice(observerIndex, 1);
		}
	}

	public notify(event: GraphEvent): void {
		for (const observer of this.observers) {
			observer.update(event);
		}
	}
}
