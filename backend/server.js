import express from 'express'
import mongoose from 'mongoose'
import personaRoutes from './routes/personaRoutes.js'
import journeyRoutes from './routes/journeyRoutes.js'
import cors from 'cors'
import User from './models/User.js'
import aiRoutes from './routes/aiRoutes.js'

const app = express()
app.use(express.json())

app.use(cors({
  origin: ['http://localhost:3001', 'http://localhost:5173'],
  credentials: true
}))

mongoose.connect('mongodb://127.0.0.1:27017/heylenny', {
  useNewUrlParser: true,
  useUnifiedTopology: true
})

app.get('/create-test-user', async (req, res) => {
  const existing = await User.findOne({ email: 'test@heylenny.com' })
  if (existing) return res.json(existing)

  const user = await User.create({ email: 'test@heylenny.com', password: '123456' })
  res.json(user)
})

app.use('/api/v1/personas', personaRoutes)
app.use('/api/v1/journeys', journeyRoutes)
app.use('/api/v1/ai', aiRoutes)

app.listen(5001, () => console.log('Express-Server läuft auf Port 5001 🚀'))
