import { GraphGenerator, GraphGeneratorConfig } from "./GraphGeneration";
import { Constructor } from "./Utility";
import { RNG } from "./NumberGenerators";

export interface TaskConfig extends GraphGeneratorConfig {
	seed: string;
}

export interface Task {}

// export type GraphConstructor<G extends Graph<Vertex, Edge, VertexParameters, EdgeParameters>> = new (args: GraphParameters) => G;
export abstract class TaskGenerator<G, C extends TaskConfig> {
	protected config: C;
	protected rng: RNG;
	protected graph: G;
	constructor(
		protected graphConstructor: Constructor<G>,
		protected graphGeneratorConstructor: Constructor<GraphGenerator<G, C>>
	) {}

	public generateTask(config: C) {
		const { seed } = config;
		this.rng = new RNG(seed);
		this.config = config;
	}
}
