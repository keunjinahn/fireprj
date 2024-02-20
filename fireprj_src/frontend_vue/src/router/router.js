import Vue from 'vue'
import VueRouter from 'vue-router'
import * as View from '@/views'
import session from '@/plugins/session'
import { Typhoon_Manage } from "../views";

async function rootAccess(to, from, next) {
  if (!session.authentication && to.query.uid) {
    try {
      await session.loginFromProp(to.query.uid)
      next({ name: 'dashboard' })
    }
    catch (e) {
      next({ name: 'dashboard' })
    }
  }
  else next({ name: 'dashboard' })
}

const beforeEnter = (to, from, next) => {
  if (session.authentication) next()
  else next({ name: 'login' })
}

Vue.use(VueRouter)

const routes = [{
  path: '/',
  name: 'home',
  template: '<router-view />',
  beforeEnter: rootAccess
},
{
  path: '/login',
  component: View.Login,
  children: [
    {
      path: '',
      name: 'login',
      component: View.Login_SignIn
    },
    {
      path: 'signup',
      name: 'signup',
      component: View.Login_SignUp
    },
    {
      path: 'find-password',
      name: 'find-password',
      component: View.Login_FindPassword
    }
  ]
},
{
  path: '/dashboard',
  name: 'dashboard',
  component: View.Dashboard,
  beforeEnter
},
{
  path: '/typhoon_manage',
  name: 'typhoon_manage',
  component: View.Typhoon_Manage,
  meta: { breadcrumb: [{ text: '모니터링', disabled: true }, { text: '태풍관리', disabled: true }] },
  props: true,
  beforeEnter
},
{
  path: '/typhoon_manage/:fstatus',
  name: 'typhoon_manage_tab',
  component: View.Typhoon_Manage,
  meta: { breadcrumb: [{ text: '모니터링', disabled: true }, { text: '태풍관리', disabled: true }] },
  props: true,
  beforeEnter
},
{
  path: '/damage_manage',
  name: 'damage_manage',
  component: View.Damage_Manage,
  meta: { breadcrumb: [{ text: '모니터링', disabled: true }, { text: '태풍 피해 관리', disabled: true }] },
  props: true,
  beforeEnter
},
{
  path: '/damage_manage/:fstatus',
  name: 'damage_manage_tab',
  component: View.Damage_Manage,
  meta: { breadcrumb: [{ text: '모니터링', disabled: true }, { text: '태풍 피해 관리', disabled: true }] },
  props: true,
  beforeEnter
},
{
  path: '/statistics',
  name: 'statistics_dashboard',
  component: View.Statistics_Dashboard,
  meta: { breadcrumb: [{ text: '통계 관리', disabled: true }, { text: '태풍 통계 현황', disabled: true }] },
  props: true,
  beforeEnter
},
{
  path: '/statistics/:fstatus',
  name: 'statistics_dashboard_tab',
  component: View.Statistics_Dashboard,
  meta: { breadcrumb: [{ text: '통계 관리', disabled: true }, { text: '태풍 통계 현황', disabled: true }] },
  props: true,
  beforeEnter
},
{
  path: '/report/',
  name: 'statistics_report',
  component: View.Statistics_Report,
  meta: { breadcrumb: [{ text: '보고서 관리', disabled: true }, { text: '세부 피해내역 보고서', disabled: true }] },
  props: true,
  beforeEnter
},
{
  path: '/report/:fstatus',
  name: 'statistics_report_tab',
  component: View.Statistics_Report,
  meta: { breadcrumb: [{ text: '보고서 관리', disabled: true }, { text: '세부 피해내역 보고서', disabled: true }] },
  props: true,
  beforeEnter
},
{
  path: '/user/',
  name: 'user_manage',
  component: View.User_Manage,
  meta: { breadcrumb: [{ text: '사용자 관리', disabled: true }, { text: '사용자 관리', disabled: true }] },
  props: true,
  beforeEnter
},
{
  path: '/user/:fstatus',
  name: 'user_manage_tab',
  component: View.User_Manage,
  meta: { breadcrumb: [{ text: '사용자 관리', disabled: true }, { text: '사용자 관리', disabled: true }] },
  props: true,
  beforeEnter
},
{
  path: '/community',
  name: 'community_list',
  component: View.Community_List,
  meta: { breadcrumb: [{ text: '커뮤니티', disabled: true }, { text: '커뮤니티', disabled: true }] },
  props: true,
  beforeEnter

},
{
  path: '/community/:fstatus',
  name: 'community_list_tab',
  component: View.Community_List,
  meta: { breadcrumb: [{ text: '커뮤니티', disabled: true }, { text: '커뮤니티', disabled: true }] },
  props: true,
  beforeEnter

}
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
