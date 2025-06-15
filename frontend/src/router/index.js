import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import SeoAudits from '@/views/SeoAudits.vue'
import SeoGenerator from '@/views/SeoGenerator.vue'
import Dashboard from '@/views/Dashboard.vue'
import AddWebsite from '@/views/AddWebsite.vue'
import ToDos from '@/views/ToDos.vue'
import Keywords from '@/views/Keywords.vue'
import KeywordIdeas from '@/views/KeywordIdeas.vue'
import CompetitorAnalysis from '@/views/CompetitorAnalysis.vue'

const routes = [
  { path: '/',           name: 'Dashboard',  component: Dashboard },
  { path: '/login',      name: 'Login',      component: Login },
  { path: '/register',   name: 'Register',   component: Register },
  { path: '/seo-audits', name: 'SeoAudits',  component: SeoAudits },
  { path: '/seo-generator', name: 'SeoGenerator', component: SeoGenerator },
  { path: '/seo/:id',    name: 'SEODetail',  component: () => import('@/views/SEODetail.vue') },
  { path: '/websites/add', name: 'add-website', component: AddWebsite },
  { path: '/keywords',   name: 'Keywords',   component: Keywords },    // <-- neu
  { path: '/todos',      name: 'ToDos',      component: ToDos },
  // Fallback: alle unbekannten Pfade auf Dashboard
  { path: '/:pathMatch(.*)*', redirect: '/' },
  { path: '/keyword-ideas', name: 'KeywordIdeas', component: KeywordIdeas },
  { path: '/competitor-analysis', name: 'CompetitorAnalysis', component: CompetitorAnalysis },
]

export default createRouter({
  history: createWebHistory(),
  routes
})
