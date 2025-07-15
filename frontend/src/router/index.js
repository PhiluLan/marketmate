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
import ChatWithLenny from "@/views/ChatWithLenny.vue";
import MetaIntegration from '@/views/MetaIntegration.vue'
import AdsOverview    from '@/views/AdsOverview.vue'
import ContentCalendar from '@/views/ContentCalendar.vue'
import PersonaBuilder from '@/views/PersonaBuilder.vue'
import JourneyVisualizer from '@/views/JourneyVisualizer.vue'
import JourneyBuilder from '@/views/JourneyBuilder.vue'
import ContentGenerateView from '@/views/ContentGenerateView.vue'
import ContentEditor from '@/views/ContentEditor.vue';
import AssetGenerateView from '@/views/AssetGenerateView.vue';
import SchedulerView         from '@/views/SchedulerView.vue'
import ContentManageView from '@/views/ContentManageView.vue'
import GoogleIntegrationView from '@/views/GoogleIntegrationView.vue'
import LandingPage   from '@/views/LandingPage.vue'
import VerifyEmail from '@/views/VerifyEmail.vue'


const routes = [
  { path: '/', name: 'Landing', component: LandingPage,},
  { path: '/dashboard',           name: 'Dashboard',  component: Dashboard },
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
  { path: "/chat", name: "ChatWithLenny", component: ChatWithLenny },
  { path:'/integrations',  component: MetaIntegration },
  { path:'/ads-overview',   component: AdsOverview },
  { path: '/content-calendar', name: 'ContentCalendar', component: ContentCalendar },
  { path: '/personas', name: 'PersonaBuilder', component: PersonaBuilder },
  { path: '/journey', name: 'Journey', component: JourneyVisualizer },
  { path: '/journey-builder', name: 'JourneyBuilder',component: JourneyBuilder },
  { path: '/generate', name: 'Generate', component: ContentGenerateView },
  { path: '/editor', name: 'ContentEditor', component: ContentEditor},
  { path: '/assets', name: 'Assets', component: AssetGenerateView },
  { path: '/scheduler', name: 'Scheduler', component: SchedulerView },
  { path: '/manage-contents', name: 'ManageContents', component: ContentManageView },
  { path: '/integrations/google', name: 'GoogleIntegration', component: GoogleIntegrationView },
  { path: '/verify-email', name: 'VerifyEmail', component: VerifyEmail},
]

export default createRouter({
  history: createWebHistory(),
  routes
})
