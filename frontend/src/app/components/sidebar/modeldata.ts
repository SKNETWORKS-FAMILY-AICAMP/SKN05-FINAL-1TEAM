interface Model {
    id: string;
    name: string;
  }
  
  interface Brand {
    id: string;
    name: string;
    models: Model[];
  }
  

export const BRANDS: Brand[] = [
    {
      id: 'Canon',
      name: 'Canon',
      models: [
        { id: '200d', name: 'Canon 200D' },
        { id: 'M50', name: 'Canon M50' },
        { id: 'R6', name: 'Canon R6' },
        { id: 'R50', name: 'Canon R50' },
        { id: 'Powershot', name: 'Canon Powershot' },
      ]
    },
    {
      id: 'Sony',
      name: 'Sony',
      models: [
        { id: 'a7', name: 'Sony a7' },
        { id: 'a6400', name: 'Sony a6400' },
        { id: 'a6600', name: 'Sony a6600' },
        { id: 'a7m3', name: 'Sony a7m3' },
        { id: 'a7m4', name: 'Sony a7m4' },
      ]
    },
    {
      id: 'Fujifilm',
      name: 'Fujifilm',
      models: [
        { id: 'x-t40', name: 'Fujifilm X-T40' },
        { id: 'x-t50', name: 'Fujifilm X-T50' },
        { id: 'x-t5', name: 'Fujifilm X-T5' },
        { id: 'x-t3', name: 'Fujifilm X-T3' },
        { id: 'x-t4', name: 'Fujifilm X-T4' },
      ]
    }
  ];
  