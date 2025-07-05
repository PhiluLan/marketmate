// routes/personaRoutes.js
import express from 'express'
import {
  createPersona,
  getPersonas,
  updatePersona,
  deletePersona
} from '../controllers/personaController.js'

import { protect } from '../middleware/auth.js'

const router = express.Router()

router.route('/')
  .get(protect, getPersonas)
  .post(protect, createPersona)

router.route('/:id')
  .put(protect, updatePersona)
  .delete(protect, deletePersona)

export default router
