import { Observable, Observer, ObservableEvent } from "./Observer";
import { Constructor } from "./Utility";
import { GraphParameters } from "./genericGraphs/Graph";
import { RNG } from "./NumberGenerators";

export interface GraphGeneratorConfig extends GraphParameters {}
export abstract class GraphGenerator<G, C extends GraphGeneratorConfig> implements Observable {
	protected observers: Array<Observer> = [];
	protected graph: G;
	protected config: C;
	protected rng: RNG;
	constructor(rng: RNG) {
		this.rng = rng;
	}
	public generateGraph(graphConstructor: Constructor<G>, config: C): G {
		this.config = config;
		this.graph = new graphConstructor(config);

		return this.graph;
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
	public notify(event: ObservableEvent): void {
		for (const observer of this.observers) {
			observer.update(event);
		}
	}
}
