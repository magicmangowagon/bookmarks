import axios from 'axios';

const API_URL = 'http://localhost:8000';

export class APIService{
    constructor(){

    }

    /* The other methods go here */
  getList () {
    const url = '${API_URL;}';
    return axios.get(url, {})
  }
}
