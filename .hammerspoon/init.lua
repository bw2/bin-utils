hs.window.animationDuration = 0
units = {
  left50        = { x = 0.00, y = 0.00, w = 0.50, h = 1.00 },
  right50       = { x = 0.50, y = 0.00, w = 0.50, h = 1.00 },
  top50         = { x = 0.00, y = 0.00, w = 1.00, h = 0.50 },
  bot50         = { x = 0.00, y = 0.50, w = 1.00, h = 0.50 },
  upleft70      = { x = 0.00, y = 0.00, w = 0.70, h = 0.50 },
  botleft70     = { x = 0.00, y = 0.50, w = 0.70, h = 0.50 },
  maximum       = { x = 0.00, y = 0.00, w = 1.00, h = 1.00 }
}


mash = { 'shift', 'cmd' }
hs.hotkey.bind(mash, 'i', function() hs.window.focusedWindow():move(units.top50,     nil, true) end)
hs.hotkey.bind(mash, 'k', function() hs.window.focusedWindow():move(units.bot50,      nil, true) end)
hs.hotkey.bind(mash, 'l', function() hs.window.focusedWindow():move(units.right50,    nil, true) end)
hs.hotkey.bind(mash, 'j', function() hs.window.focusedWindow():move(units.left50,      nil, true) end)
hs.hotkey.bind(mash, 'm', function() hs.window.focusedWindow():move(units.maximum,    nil, true) end)




-------------------------------------------------------------------
-- Launcher
--
-- This is the awesome. The other stuff is all cool, but this is the
-- thing I love the most because it reduces the amount of time I
-- spend with the mouse, and is far more deterministic than trying
-- to use cmd+tab.
--
-- The idea here is to have a MODE-BASED app launching and app
-- switching system. Traditional Mac philosophy (and Emacs :D)
-- would have us contort our hands into crazy combinations of keys
-- to manipulate the state of the machine, which is a serious pain
-- in the ass. Using Hammerspoon we can avoid that.
--
-- * ctrl+space gets us into "launch mode"
-- * In "launch mode" the keyboard changes so that each key can now
--   have a new meaning. For example, the 'v' key is now responsible
--   for either launching or switching to VimR
-- * You can then map whatever you like to whatever function you'd
--   like to invoke.
--
-- It's just a big pile of awesome.
-------------------------------------------------------------------

-- We need to store the reference to the alert window
appLauncherAlertWindow = nil

-- This is the key mode handle
launchMode = hs.hotkey.modal.new({}, nil, '')

-- Leaves the launch mode, returning the keyboard to its normal
-- state, and closes the alert window, if it's showing
function leaveMode()
  if appLauncherAlertWindow ~= nil then
    hs.alert.closeSpecific(appLauncherAlertWindow, 0)
    appLauncherAlertWindow = nil
  end
  launchMode:exit()
end

-- So simple, so awesome.
function switchToApp(app)
  hs.application.open(app)
  leaveMode()
end

-- Enters launch mode. The bulk of this is geared toward
-- showing a big ugly window that can't be ignored; the
-- keyboard is now in launch mode.
hs.hotkey.bind({ 'shift' }, 'space', function()
  launchMode:enter()
  appLauncherAlertWindow = hs.alert.show('App Launcher Mode', {
    strokeColor = hs.drawing.color.x11.orangered,
    fillColor = hs.drawing.color.x11.white,
    textColor = hs.drawing.color.x11.black,
    strokeWidth = 20,
    radius = 30,
    textSize = 30,
    fadeInDuration = 0,
    atScreenEdge = 0
  }, 'infinite')
end)

-- When in launch mode, hitting ctrl+space again leaves it
launchMode:bind({ 'shift' }, 'space', function() leaveMode() end)

-- Mapped keys
launchMode:bind({}, 'c',  function() switchToApp('Google Chrome.app') end)
launchMode:bind({}, 'f',  function() switchToApp('Firefox.app') end)
launchMode:bind({}, 'k',  function() switchToApp('Skim.app') end)
launchMode:bind({}, 'e',  function() switchToApp('Microsoft Excel.app') end)

launchMode:bind({}, 's',  function() switchToApp('Slack.app') end)
launchMode:bind({}, 'i',  function() switchToApp('IntelliJ IDEA.app') end)
launchMode:bind({}, 't',  function() switchToApp('iTerm.app') end)
launchMode:bind({}, '`',  function() hs.reload(); leaveMode() end)

-- launchMode:bind({}, 'i',  function() switchToApp('Signal.app') end)
-- launchMode:bind({}, 'p',  function() switchToApp('Microsoft Powerpoint.app') end)
-- launchMode:bind({}, 'v',  function() switchToApp('VimR.app') end)
-- launchMode:bind({}, 'v',  function() switchToApp('MacVim.app') end)
-- launchMode:bind({}, 'w',  function() switchToApp('WhatsApp.app') end)

-- Unmapped keys
launchMode:bind({}, 29,  function() leaveMode() end)
launchMode:bind({}, 'b',  function() leaveMode() end)
launchMode:bind({}, 'h',  function() leaveMode() end)
launchMode:bind({}, 'j',  function() leaveMode() end)
launchMode:bind({}, 'n',  function() leaveMode() end)
launchMode:bind({}, 'q',  function() leaveMode() end)
launchMode:bind({}, 'u',  function() leaveMode() end)
launchMode:bind({}, 'x',  function() leaveMode() end)
launchMode:bind({}, 'y',  function() leaveMode() end)
launchMode:bind({}, '1',  function() leaveMode() end)
launchMode:bind({}, '2',  function() leaveMode() end)
launchMode:bind({}, '3',  function() leaveMode() end)
launchMode:bind({}, '4',  function() leaveMode() end)
launchMode:bind({}, '5',  function() leaveMode() end)
launchMode:bind({}, '6',  function() leaveMode() end)
launchMode:bind({}, '7',  function() leaveMode() end)
launchMode:bind({}, '8',  function() leaveMode() end)
launchMode:bind({}, '9',  function() leaveMode() end)
launchMode:bind({}, '0',  function() leaveMode() end)
launchMode:bind({}, '-',  function() leaveMode() end)
launchMode:bind({}, '=',  function() leaveMode() end)
launchMode:bind({}, '[',  function() leaveMode() end)
launchMode:bind({}, ']',  function() leaveMode() end)
launchMode:bind({}, '\\', function() leaveMode() end)
launchMode:bind({}, ';',  function() leaveMode() end)
launchMode:bind({}, "'",  function() leaveMode() end)
launchMode:bind({}, ',',  function() leaveMode() end)
launchMode:bind({}, '.',  function() leaveMode() end)
launchMode:bind({}, '/',  function() leaveMode() end)