import { message } from 'antd';
import axios from 'axios';

export const getAllCars = () => async (dispatch) => {
  dispatch({ type: 'LOADING', payload: true });

  try {
    const response = await axios.get('/api/cars/getallcars');
    dispatch({ type: 'GET_ALL_CARS', payload: response.data });
    dispatch({ type: 'LOADING', payload: false });
  } catch (error) {
    console.error('Error retrieving all cars:', error);
    dispatch({ type: 'LOADING', payload: false });
    message.error('Failed to retrieve car data. Please try again later.');
  }
};

export const addCar = (reqObj) => async (dispatch) => {
  dispatch({ type: 'LOADING', payload: true });

  try {
    await axios.post('/api/cars/addcar', reqObj);

    dispatch({ type: 'LOADING', payload: false });
    message.success('New car added successfully');
    setTimeout(() => {
      window.location.href = '/';
    }, 500);
  } catch (error) {
    console.error('Error adding new car:', error);
    dispatch({ type: 'LOADING', payload: false });
    message.error('Failed to add new car. Please try again later.');
  }
};

export const editCar = (reqObj) => async (dispatch) => {
  dispatch({ type: 'LOADING', payload: true });

  try {
    await axios.post('/api/cars/editcar', reqObj);

    dispatch({ type: 'LOADING', payload: false });
    message.success('Car details updated successfully');
    setTimeout(() => {
      window.location.href = '/admin';
    }, 500);
  } catch (error) {
    console.error('Error editing car details:', error);
    dispatch({ type: 'LOADING', payload: false });
    message.error('Failed to update car details. Please try again later.');
  }
};

export const deleteCar = (reqObj) => async (dispatch) => {
  dispatch({ type: 'LOADING', payload: true });

  try {
    await axios.delete(`/api/cars/deletecar/${reqObj.carid}`);

    dispatch({ type: 'LOADING', payload: false });
    message.success('Car deleted successfully');
    setTimeout(() => {
      window.location.reload();
    }, 500);
  } catch (error) {
    console.error('Error deleting car:', error);
    dispatch({ type: 'LOADING', payload: false });
    message.error('Failed to delete car. Please try again later.');
  }
};
