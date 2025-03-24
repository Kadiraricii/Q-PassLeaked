from ux.parent import PentestApp, ParentUX
from ux.dashboard import DashboardScreen
from ux.nmap import NmapScreen

if __name__ == '__main__':
    app = PentestApp()
    parent = ParentUX()
    parent.screen_manager.add_widget(DashboardScreen(name='dashboard'))
    parent.screen_manager.add_widget(NmapScreen(name='nmap'))
    parent.screen_manager.current = 'dashboard'
    app.run()