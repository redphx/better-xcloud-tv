if (window.location.pathname.startsWith('/oauth20_authorize.srf')) {
    window.location = 'https://www.xbox.com/play/login/deviceCode';
    throw new Error('[Better xCloud] Ignore');
}

if (!window.location.pathname.includes('/play')) {
    throw new Error('[Better xCloud] Ignore');
}

window.BX_FLAGS = {
    CheckForUpdate: false,
    SafariWorkaround: false,
    ScriptUi: 'tv',
};
