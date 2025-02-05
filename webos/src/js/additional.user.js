if (window.location.pathname.startsWith('/oauth20_authorize.srf')) {
    window.location = 'https://www.xbox.com/en-US/play/login/deviceCode';
    throw new Error('[Better xCloud] Ignore');
}

if (!window.location.pathname.includes('/play')) {
    throw new Error('[Better xCloud] Ignore');
}

window.BX_FLAGS = {
    CheckForUpdate: false,
    SafariWorkaround: false,

    DeviceInfo: {
        deviceType: 'webos',
    },
};
