export interface Observer {
	update(event: ObservableEvent): void;
}

export interface Observable {
	attach(observer: Observer): void;
	detach(observer: Observer): void;
	notify(event: ObservableEvent): void;
}

export interface ObservableEvent {
	type: string;
	data: any;
}
