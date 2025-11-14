import streamlit as st
import numpy as np
from scipy.spatial import ConvexHull, QhullError
import plotly.graph_objects as go
import string
import re
from h_categorizer import sample_and_compute_X


def _safe_hull(points, qhull_opts='QJ', jitter=1e-8):
    """
    Try to build a convex hull robustly.
    1) try with QJ (joggle)
    2) try with tiny jitter
    3) if still failing, return None
    """
    try:
        return ConvexHull(points, qhull_options=qhull_opts)
    except QhullError:
        try:
            pts = points + jitter * np.random.randn(*points.shape)
            return ConvexHull(pts, qhull_options=qhull_opts)
        except QhullError:
            return None


def compute(A, R, n_samples, valAxe, controlled_args):
    """Compute and visualize convex hull projections."""
    X_res = sample_and_compute_X(
        A, R, max_iter=1000, n_samples=n_samples, controlled_args=controlled_args)

    # Build a full-dimensional hull only if |A| > 1
    if len(A) > 1:
        convHull = _safe_hull(X_res)
        if convHull is None:
            st.warning("Convex hull in full dimension is degenerate (lower-dimensional point cloud). "
                       "Proceeding without full-dimensional hull.")
    else:
        convHull = None

    match len(A):
        case 1:
            st.subheader("Projection for |A| = 1")
            x_vals = X_res[:, 0]
            x_min, x_max = np.min(x_vals), np.max(x_vals)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_vals, y=[0]*len(x_vals), mode='markers',
                                     marker=dict(size=6, opacity=0.6), name='Samples'))
            fig.add_trace(go.Scatter(x=[x_min, x_max], y=[0, 0], mode='lines',
                                     line=dict(color='white', width=1), name='Convex Hull'))
            # fig.update_layout(title=f"1D Convex Hull ({A[0]})",
            #                   xaxis_title=A[0], yaxis=dict(visible=False),
            #                   template='plotly_dark')

            fig.update_layout(
                title=f"1D Convex Hull ({A[0]})",
                xaxis_title=A[0],
                yaxis=dict(visible=False),
                showlegend=True,
                height=400,
                template='plotly_dark'
            )

            st.plotly_chart(fig, use_container_width=True)

        case 2:
            st.subheader("Projection for |A| = 2")
            # Build a 2D hull directly on 2D data for stability
            hull_2d = _safe_hull(X_res)
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=X_res[:, 0],
                y=X_res[:, 1],
                mode='markers',
                marker=dict(size=5, opacity=0.6),
                name='Points'
            ))

            if hull_2d is not None:
                vertices = hull_2d.vertices
                x_hull = hull_2d.points[vertices, 0].tolist(
                ) + [hull_2d.points[vertices[0], 0]]
                y_hull = hull_2d.points[vertices, 1].tolist(
                ) + [hull_2d.points[vertices[0], 1]]

                fig.add_trace(go.Scatter(
                    x=x_hull, y=y_hull, mode='lines+markers',
                    # permet de colorier l'intérieur du hull
                    line=dict(color='white', width=1),
                    marker=dict(size=5),
                    name='Convex Hull'
                ))
            else:
                st.info(
                    "2D hull is degenerate (colinear points). Showing points only.")

            # fig.update_layout(
            #     title=f"2D Projection ({valAxe[0]}, {valAxe[1]})",
            #     xaxis_title=A[0], yaxis_title=A[1],
            #     template='plotly_dark', height=800)

            fig.update_layout(
                xaxis_title=A[0],
                yaxis_title=A[1],
                title=dict(
                    text=(
                        f"2D Projection of ({valAxe[0]}, {valAxe[1]})<br>"
                        f"<sup>Convex Hull: Volume = {convHull.volume:.3f}, "
                        f"Surface = {convHull.area:.3f}</sup>"
                    ),
                    x=0.5,  # centre le titre
                    xanchor='center',
                    yanchor='top',
                    font=dict(size=18)
                ),
                showlegend=True,
                template='plotly_dark',
                height=1000
            )

            # Affichage
            st.plotly_chart(fig, use_container_width=True)

        case _:
            # handle 3D and higher (always project to 3D on selected axes)
            st.subheader(f"Projection for |A| = {len(A)}")

            # Select the first three axes for 3D projection
            x_axe, y_axe, z_axe = valAxe[:3]
            idx = [A.index(x_axe), A.index(y_axe), A.index(z_axe)]

            # Project the data onto the selected axes
            Xp = X_res[:, idx]

            # Try a 3D hull on the projected data
            hull_proj = _safe_hull(Xp)

            fig = go.Figure()

            # Scatter plot of points
            fig.add_trace(go.Scatter3d(
                x=Xp[:, 0],
                y=Xp[:, 1],
                z=Xp[:, 2],
                mode='markers',
                marker=dict(size=3, opacity=0.6),
                name='Points'
            ))

            # Mesh3d for convex hull if available
            if hull_proj is not None:
                fig.add_trace(go.Mesh3d(
                    x=hull_proj.points[:, 0],
                    y=hull_proj.points[:, 1],
                    z=hull_proj.points[:, 2],
                    i=hull_proj.simplices[:, 0],
                    j=hull_proj.simplices[:, 1],
                    k=hull_proj.simplices[:, 2],
                    color='white', opacity=0.1, name='Convex Hull'
                ))
            else:
                # If still degenerate (e.g., one axis constant), just show scatter
                st.info("Projected 3D hull is degenerate (points lie in a plane/line). "
                        "Showing point cloud only. Adjust sliders/relations to add variation.")

            fig.update_layout(
                scene=dict(
                    xaxis_title=x_axe,
                    yaxis_title=y_axe,
                    zaxis_title=z_axe
                ),
                title=f"3D Projection of ({x_axe}, {y_axe}, {z_axe})",
                template='plotly_dark', height=1000
            )

            # Affichage
            st.plotly_chart(fig, use_container_width=True)


def main():
    st.set_page_config(layout="wide")
    st.title("Interactive Convex Hull Visualization for Weighted h-Categorizer")

    # Basic settings
    n_args = st.slider("Number of Arguments (|A|)", 1, 10, 3)
    n_samples = st.slider("Number of Samples", 100, 100000, 500)
    A = list(string.ascii_uppercase)[:n_args]
    st.write(f"**Arguments in A:** {A}")

    # Attacks
    st.write("**Enter attack relations R as:** `(A,B),(B,C),(C,D)`")
    inputAtt = st.text_input("Relations R:")
    pattern = r"\(([A-Za-z]),\s*([A-Za-z])\)"
    matches = re.findall(pattern, inputAtt.upper())
    R = [(a, b) for a, b in matches if a in A and b in A]
    st.write(f"Attacks R: {R}")

    # Axes and controlled args
    if len(A) > 3:
        x = st.selectbox("X axis", A, index=0)
        y = st.selectbox("Y axis", A, index=1)
        z = st.selectbox("Z axis", A, index=2)
        valAxe = [x, y, z]
    else:
        valAxe = A

    controlled_args = {}
    for arg in A:
        if arg not in valAxe:
            controlled_args[arg] = st.slider(
                f"Set weight for {arg}", 0.0, 1.0, 0.5, 0.01)

    if st.button("Compute"):
        compute(A, R, n_samples, valAxe, controlled_args)


if __name__ == "__main__":
    main()
