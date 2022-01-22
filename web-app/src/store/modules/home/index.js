export default {
    namespaced: true,
    state: {
        unread: "",
        activeMenu: "1"
    },
    getters: {
        //
    },
    mutations: {
        updateUnread(state, unread) {
            state.unread = unread
        },
        updateActiveMenu(state, activeMenu) {
            state.activeMenu = activeMenu
        }
    },
}