export type Searches = Record<string, string | boolean>;

export function unique<T>(value: T, index: number, array: T[]): boolean {
  return array.indexOf(value) === index;
}
