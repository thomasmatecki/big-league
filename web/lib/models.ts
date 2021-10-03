export interface IFoo {
  id?: number;
  
}

export class Foo implements IFoo {
  constructor(id: number) {
    this.id = id;
  }
  id: number;
}
