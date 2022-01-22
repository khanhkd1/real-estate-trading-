import router from "../../../router";

export default {
    namespaced: true,
    state: {
        isAuthenticated: false,
        authUser: {},
        accessToken: '',
    },
    mutations: {
        updateLoginStatus(state, isAuthenticated) {
            state.isAuthenticated = isAuthenticated
        },
        updateAuthUser(state, authUser) {
            state.authUser = authUser
        },
        updateAccessToken(state, token) {
            state.accessToken = token
        },
        updatePermissions(state, permissions){
            state.permissions = permissions
        }
    },
    actions: {
        logout({commit}) {
            commit('updateLoginStatus', false)
            commit('updateAuthUser', {})
            commit('updateAccessToken', '')
            return router.push({name: 'Login'})
        }
    }
}