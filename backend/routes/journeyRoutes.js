// routes/journeyRoutes.js
import express from 'express'
import {
  getJourneys,
  createJourney,
  updateJourney,
  deleteJourney
} from '../controllers/journeyController.js'

import { protect } from '../middleware/auth.js'

const router = express.Router()

router.route('/')
  .get(protect, getJourneys)
  .post(protect, createJourney)

router.route('/:id')
  .put(protect, updateJourney)
  .delete(protect, deleteJourney)

export default router
