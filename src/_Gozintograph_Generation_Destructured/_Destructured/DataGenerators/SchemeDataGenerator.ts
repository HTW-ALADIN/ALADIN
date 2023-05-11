import "reflect-metadata";

// see https://fakerjs.dev/api/ for all supported mockdata fields
import {
	faker,
	NameDefinitions,
	DateDefinitions,
	WordDefinitions,
	ColorDefinitions,
	MusicDefinitions,
	LoremDefinitions,
	AnimalDefinitions,
	HackerDefinitions,
	LocaleDefinition,
	SystemDefinitions,
	AddressDefinitions,
	CompanyDefinitions,
	FinanceDefinitions,
	ScienceDefinitions,
	VehicleDefinitions,
	DatabaseDefinitions,
	CommerceDefinitions,
	InternetDefinitions,
	DateEntryDefinition,
	NameTitleDefinitions,
	PhoneNumberDefinitions,
	CommerceProductNameDefinitions,
	SystemMimeTypeEntryDefinitions,
	FinanceCurrencyEntryDefinitions,
} from "@faker-js/faker";
// see https://github.com/boo1ean/casual for all supported mockdata fields
import casual from "casual";
// see https://chancejs.com/index.html for all supported mockdata fields
var Chance = require("chance");
// see https://github.com/fent/randexp.js for the syntax of random RegExp Generators
import RandExp from "randexp";

import seedrandom from "seedrandom";

const seed = "321";
const rng = seedrandom(seed);
const numericSeed = rng.double();

const randInt = (min: number, max: number) => {
	return Math.round(rng() * (max - min) + min);
};
RandExp.prototype.randInt = randInt;

const seededChance = new Chance(seed);

faker.seed(numericSeed);
const fakerLocales = faker.locales;
const availableFakerLocales = Object.keys(fakerLocales);

type FakerMethods = {};
type CustomDataGenerator = {};

interface FakeDataSchema {
	[property: string]: {
		function: (args: Array<any>) => {};
	};
}

class ValueFactory {
	constructor() {}
}

class CollectionFactory {}
