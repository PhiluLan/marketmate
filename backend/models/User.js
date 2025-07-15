// backend/models/User.js
import mongoose from 'mongoose'

const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true
  },
  password: {
    type: String,
    required: true
  },
  firstName: {
    type: String,
    required: true,
    trim: true
  },
  lastName: {
    type: String,
    required: true,
    trim: true
  },
  websiteUrl: {
    type: String,
    required: true,
    trim: true
  },
  heyLennySummary: {
    type: String,
    default: null
  },
  isActive: {
    type: Boolean,
    default: false
  },
  emailVerifyToken: {
    type: String,
    select: false
  }
}, { timestamps: true })

const User = mongoose.model('User', userSchema)
export default User
