// src/services/AssetService.js
import api from '@/api/api';

export default {
  /**
   * Fordert die Bilderzeugung an.
   * @param {{prompt:string, n:number, size:string}} payload
   * @returns {Promise<string[]>} Liste von Bild-URLs
   */
  generateAssets(payload) {
    return api
      .post('assets/generate/', payload)
      .then(res => res.data.images);
  }
};
