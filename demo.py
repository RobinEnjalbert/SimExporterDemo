from os.path import join
import Sofa, Sofa.Gui

from SimExporter.sofa import Exporter

from simulation import Simulation
from publish import publish


if __name__ == '__main__':

    # Create the SOFA simulation
    node = Sofa.Core.Node()
    node.addObject(Simulation(root=node))

    # Create the Exporter and add objects
    exporter = Exporter(root=node, dt=0.2, animation=True, fps=80)
    exporter.objects.add_points(positions=node.logo.state.position.value[node.logo.constraints.indices.value],
                                point_size=0.3,
                                alpha=1,
                                color='#741b47',
                                dot_shading=True)
    exporter.objects.add_sofa_mesh(positions_data=node.logo.visual.ogl.position,
                                   cells=node.logo.visual.ogl.triangles.value,
                                   flat_shading=False,
                                   color='#ff7800',
                                   alpha=0.9)
    exporter.objects.add_sofa_mesh(positions_data=node.logo.state.position,
                                   cells=node.logo.topology.triangles.value,
                                   wireframe=False,
                                   color='#ff7800',
                                   alpha=0.1)

    # Init the SOFA simulation AFTER creating the exporter (otherwise, callbacks will not work)
    Sofa.Simulation.init(node)

    # Launch the SOFA Gui, run a few time steps
    Sofa.Gui.GUIManager.Init(program_name="main", gui_name="qglviewer")
    Sofa.Gui.GUIManager.createGUI(node, __file__)
    Sofa.Gui.GUIManager.SetDimension(1200, 900)
    Sofa.Gui.GUIManager.MainLoop(node)
    Sofa.Gui.GUIManager.closeGUI()

    # Export to HTML file
    exporter.set_camera(factor=1.2)
    exporter.to_html(filename=join('html', 'logo.html'), background_color='#fedfbe', grid_visible=False,
                     menu_visible=True, frame_visible=True)

    # Publish
    publish()
