/**
 * Modern JavaScript examples showcasing ES6+ features
 * 
 * This file demonstrates various JavaScript features that work
 * seamlessly with TypeScript in this project.
 */

// ======================
// Arrow Functions
// ======================
const add = (a, b) => a + b;
const square = x => x * x;

// ======================
// Destructuring
// ======================
const user = { name: 'John', age: 30, email: 'john@example.com' };
const { name, age } = user;

const numbers = [1, 2, 3, 4, 5];
const [first, second, ...rest] = numbers;

// ======================
// Spread Operator
// ======================
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const combined = [...arr1, ...arr2];

const person = { name: 'Alice', age: 25 };
const employee = { ...person, role: 'Developer', company: 'TechCorp' };

// ======================
// Template Literals
// ======================
const greeting = `Hello, ${name}! You are ${age} years old.`;
const multiline = `
  This is a
  multi-line
  string
`;

// ======================
// Default Parameters
// ======================
function greet(name = 'Guest', greeting = 'Hello') {
  return `${greeting}, ${name}!`;
}

// ======================
// Rest Parameters
// ======================
function sum(...numbers) {
  return numbers.reduce((total, num) => total + num, 0);
}

// ======================
// Object Property Shorthand
// ======================
const username = 'bob';
const userAge = 28;
const userObj = { username, userAge };

// ======================
// Computed Property Names
// ======================
const propertyName = 'email';
const obj = {
  [propertyName]: 'test@example.com',
  [`${propertyName}Verified`]: true
};

// ======================
// Promises and Async/Await
// ======================
const fetchData = async () => {
  try {
    const response = await fetch('https://api.example.com/data');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
};

// ======================
// Array Methods
// ======================
const items = [1, 2, 3, 4, 5];

const doubled = items.map(x => x * 2);
const filtered = items.filter(x => x > 2);
const found = items.find(x => x === 3);
const total = items.reduce((sum, x) => sum + x, 0);
const hasEven = items.some(x => x % 2 === 0);
const allPositive = items.every(x => x > 0);

// ======================
// Optional Chaining
// ======================
const userData = {
  profile: {
    address: {
      city: 'New York'
    }
  }
};

const city = userData?.profile?.address?.city;
const country = userData?.profile?.address?.country ?? 'Unknown';

// ======================
// Nullish Coalescing
// ======================
const value1 = null ?? 'default';
const value2 = undefined ?? 'default';
const value3 = 0 ?? 'default'; // Returns 0, not 'default'

// ======================
// Class Syntax
// ======================
class Animal {
  constructor(name) {
    this.name = name;
  }

  speak() {
    return `${this.name} makes a sound`;
  }
}

class Dog extends Animal {
  constructor(name, breed) {
    super(name);
    this.breed = breed;
  }

  speak() {
    return `${this.name} barks`;
  }
}

// ======================
// Modules (ES6)
// ======================
// Export examples:
export const PI = 3.14159;
export function calculateArea(radius) {
  return PI * radius * radius;
}

export default class Calculator {
  add(a, b) {
    return a + b;
  }

  subtract(a, b) {
    return a - b;
  }
}

// ======================
// Set and Map
// ======================
const uniqueNumbers = new Set([1, 2, 2, 3, 4, 4, 5]);
const map = new Map([
  ['key1', 'value1'],
  ['key2', 'value2']
]);

// ======================
// Symbol
// ======================
const sym1 = Symbol('description');
const sym2 = Symbol('description');
// sym1 !== sym2

// ======================
// Generators
// ======================
function* numberGenerator() {
  yield 1;
  yield 2;
  yield 3;
}

const gen = numberGenerator();
// gen.next().value => 1
// gen.next().value => 2

// ======================
// for...of Loop
// ======================
const iterableArray = [10, 20, 30];
for (const value of iterableArray) {
  console.log(value);
}

// ======================
// Object.entries() and Object.keys()
// ======================
const object = { a: 1, b: 2, c: 3 };
const entries = Object.entries(object);
const keys = Object.keys(object);
const values = Object.values(object);

// ======================
// Array.flat() and Array.flatMap()
// ======================
const nested = [1, [2, 3], [4, [5, 6]]];
const flattened = nested.flat(2);

const mapped = [1, 2, 3].flatMap(x => [x, x * 2]);

// ======================
// String Methods
// ======================
const str = '  Hello World  ';
const trimmed = str.trim();
const starts = str.startsWith('  Hello');
const ends = str.endsWith('World  ');
const includes = str.includes('World');
const repeated = 'abc'.repeat(3);

// ======================
// Promise.all() and Promise.race()
// ======================
const promise1 = Promise.resolve(1);
const promise2 = Promise.resolve(2);
const promise3 = Promise.resolve(3);

Promise.all([promise1, promise2, promise3])
  .then(values => console.log(values)); // [1, 2, 3]

Promise.race([promise1, promise2, promise3])
  .then(value => console.log(value)); // 1 (first resolved)

// ======================
// Dynamic Import
// ======================
async function loadModule() {
  const module = await import('./some-module.js');
  module.doSomething();
}
