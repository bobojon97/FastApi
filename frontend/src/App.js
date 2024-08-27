import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { MaterialReactTable } from 'material-react-table';
import { Select, MenuItem, Box } from '@mui/material';
import dayjs from 'dayjs';

const Example = () => {
  const [data, setData] = useState([]);
  const [regions, setRegions] = useState([]);
  const [selectedRegion, setSelectedRegion] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/battery-data/', {
          params: { region: selectedRegion },
          timeout: 180000, // Увеличение времени ожидания до 3 минут
        });

        console.log('Полный ответ от бэкенда:', response.data);
        setData(response.data.battery_data || []);
        setRegions(response.data.regions || []);
      } catch (error) {
        console.error('Ошибка при загрузке данных:', error.response || error.message);
      }
    };

    fetchData();
  }, [selectedRegion]);

  // Форматирование числа с двумя десятичными знаками
  const formatNumber = (value) => {
    if (typeof value === 'number') {
      return value.toFixed(2);
    }
    return value;
  };

  // Форматирование даты и времени
  const formatDate = (timestamp) => {
    return dayjs(timestamp).format('YYYY-MM-DD HH:mm');
  };

  const columns = useMemo(
    () => [
      {  accessorKey: 'controller_name', 
        header: 'Controller name', 
        size: 80,
        Cell: ({ cell }) => {
          const controllerName = cell.getValue();
          return (
            <a href={`http://localhost:3000/controller/${controllerName}`} target="_blank" rel="noopener noreferrer">
              {controllerName}
            </a>
          );
        },
      },
      { 
        accessorKey: 'data.Avg_Batt_Volt', 
        header: 'Batt Volt', 
        size: 50,
        Cell: ({ cell }) => formatNumber(cell.getValue()),
      },
      { 
        accessorKey: 'data.Sum_Batt_Curr', 
        header: 'Batt Curr', 
        size: 50,
        Cell: ({ cell }) => formatNumber(cell.getValue()),
      },
      { 
        accessorKey: 'data.Avg_SOC', 
        header: 'SOC', 
        size: 50,
        Cell: ({ cell }) => formatNumber(cell.getValue()),
      },
      { 
        accessorKey: 'data.Avg_SOH', 
        header: 'SOH', 
        size: 50,
        Cell: ({ cell }) => formatNumber(cell.getValue()),
      },
      { 
        accessorKey: 'data.Avg_Cycle', 
        header: 'Cycle', 
        size: 50,
        Cell: ({ cell }) => formatNumber(cell.getValue()),
      },
      { 
        accessorKey: 'data.Avg_Mos_Temp', 
        header: 'Mos Temp', 
        size: 50,
        Cell: ({ cell }) => formatNumber(cell.getValue()),
      },
      { 
        accessorKey: 'data.Avg_Env_Temp', 
        header: 'Env Temp', 
        size: 50,
        Cell: ({ cell }) => formatNumber(cell.getValue()),
      },
      { 
        accessorKey: 'data.Avg_Full_Capacity', 
        header: 'Full Capacity', 
        size: 100,
        Cell: ({ cell }) => formatNumber(cell.getValue()),
      },
      { 
        accessorKey: 'data.Avg_Remaining_Capacity', 
        header: 'Remaining Capacity', 
        size: 100,
        Cell: ({ cell }) => formatNumber(cell.getValue()),
      },
      { 
        accessorKey: 'data.Avg_Temp_Max_Cell', 
        header: 'Temp Max Cell', 
        size: 100,
        Cell: ({ cell }) => formatNumber(cell.getValue()),
      },
      { 
        accessorKey: 'data.Avg_Temp_Min_Cell', 
        header: 'Temp Min Cell', 
        size: 100,
        Cell: ({ cell }) => formatNumber(cell.getValue()),
      },
      {
        accessorKey: 'region',
        header: (
          <Box display="flex" alignItems="center" sx={{ lineHeight: '0.2' }}>
            <span style={{ marginTop: '-12px' }}>Regions</span>
            <Select
              value={selectedRegion}
              onChange={(e) => setSelectedRegion(e.target.value)}
              variant="outlined"
              size="small"
              displayEmpty
              sx={{ marginLeft: '8px', fontSize: '0.875rem' }}
            >
              <MenuItem value="">All Regions</MenuItem>
              {regions.map((region) => (
                <MenuItem key={region} value={region}>
                  {region}
                </MenuItem>
              ))}
            </Select>
          </Box>
        ),
        size: 150,
      },
      { accessorKey: 'dga', header: 'DGA', size: 50 },
      { accessorKey: 'dga_real_status', header: 'DGA Real Status', size: 100 },
      {
        accessorKey: 'timestamp',
        header: 'Time',
        size: 150,
        Cell: ({ cell }) => formatDate(cell.getValue()), // Форматирование даты и времени
      },
    ],
    [selectedRegion, regions],
  );

  return (
    <MaterialReactTable
      columns={columns}
      data={data}
      enableColumnResizing={false}
      enableColumnOrdering={false}
      enableColumnActions={false}
      enableRowSelection={false}
      enableSorting={false}
      muiTableHeadCellProps={{
        sx: {
          padding: '0px 4px',
        },
      }}
      muiTableContainerProps={{
        sx: {
          maxHeight: 'none',
        },
      }}
    />
  );
};

export default Example;