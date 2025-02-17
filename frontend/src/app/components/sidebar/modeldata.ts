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
        { id: 'EOS 200D II', name: 'EOS 200D II' },
        { id: 'EOS M50 Mark II', name: 'EOS M50 Mark II' },
        { id: 'EOS R50 Mark II', name: 'EOS R50 Mark II' },
        { id: 'EOS R6', name: 'EOS R6' },
        { id: 'PowerShot G7X Mark III', name: 'PowerShot G7X Mark III' },
      ]
    },
    {
      id: 'Sony',
      name: 'Sony',
      models: [
        { id: 'ILCE-6400 a6400', name: 'ILCE-6400 a6400' },
        { id: 'ILCE-7M3 a7III', name: 'ILCE-7M3 a7III' },
        { id: 'DSC-RX100M7', name: 'DSC-RX100M7' },
        { id: 'ZV-1', name: 'ZV-1' },
        { id: 'ZV-E10', name: 'ZV-E10' },
      ]
    },
    {
      id: 'Fuji',
      name: 'Fuji',
      models: [
        { id: 'gfx100ii', name: 'gfx100ii' },
        { id: 'x-e4', name: 'x-e4' },
        { id: 'x-s20', name: 'x-s20' },
        { id: 'x-t5', name: 'x-t5' },
        { id: 'x100v', name: 'x100v' },
      ]
    }
  ];
  