from os.path import join
from numpy import load, zeros, log10
from numpy.linalg import norm
import Sofa
import Sofa.Gui

from SimExporter.sofa import Exporter
from simulation import Simulation
from publish import publish


if __name__ == '__main__':


    # Create the SOFA simulation
    node = Sofa.Core.Node()
    node.addObject(Simulation(root=node))

    def force():
        if len(node.logo.state.force.value) != len(node.logo.state.position.value):
            return zeros((len(node.logo.state.position.value),))
        return log10(norm(node.logo.state.force.value, axis=1) + 1)

    # Create the Exporter and add objects
    exporter = Exporter(root=node, dt=0.2, animation=True, fps=60)
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
                                   alpha=0.1,
                                   # colormap_name='jet',
                                   # colormap_function=force,
                                   colormap_range=[0, 5])

    # Init the SOFA simulation AFTER creating the exporter (otherwise, callbacks will not work)
    Sofa.Simulation.init(node)

    # Launch the SOFA Gui, run a few time steps
    Sofa.Gui.GUIManager.Init(program_name="main", gui_name="qglviewer")
    Sofa.Gui.GUIManager.createGUI(node, __file__)
    Sofa.Gui.GUIManager.SetDimension(1200, 900)
    Sofa.Gui.GUIManager.MainLoop(node)
    Sofa.Gui.GUIManager.closeGUI()

    # Export to HTML file
    exporter.set_camera(factor=0.8)
    exporter.to_html(filename=join('html', 'logo.html'), background_color='#353535', grid_visible=False,
                     menu_visible=True, frame_visible=True)

    # Publish
    # publish()
