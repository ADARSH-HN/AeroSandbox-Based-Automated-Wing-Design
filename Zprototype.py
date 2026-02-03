import os
import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p
from matplotlib.colors import LinearSegmentedColormap
from aerosandbox.tools.string_formatting import eng_string
import pandas as pd



folder=r"E:\\Aeroclub\\Airfoils_twst"
output_file = "E:\\Aeroclub\\software\\neuralfoil_output.csv"

if os.path.exists(output_file):
    os.remove(output_file)

# Main inputs 
MTOW_kgs=8.5  # Maximum Takeoff Weight in kilograms userinput 
Max_wingspan_limit=1.8  # Maximum Wingspan in meters userinput
velocity=13 # m/s
aspect_ratios = [3, 4, 5, 6, 7]


MTOW_newtons = MTOW_kgs * 9.81  # Maximum Takeoff Weight in Newtons

for file in os.listdir(folder):
    if file.endswith(".dat"):
        file_name=os.path.join(folder,file)
        af=asb.Airfoil(file_name)
        af=af.to_kulfan_airfoil()
        # af.draw() #optionally show airfoil
        alpha_diff=0.1 
        alpha = np.linspace(-10, 20, int((20 - (-10)) / alpha_diff) + 1)
        re = np.geomspace(1.5e5, 4e5, 10) 
        Alpha, Re = np.meshgrid(alpha, re)
        mach = velocity / 343  
        res=af.get_aero_from_neuralfoil(alpha=Alpha.flatten(),Re=Re.flatten(),mach=mach,model_size="xxxlarge")
        Aero = {key: value.reshape(Alpha.shape) for key, value in res.items()}
        colors = LinearSegmentedColormap.from_list("custom_cmap",colors=[p.adjust_lightness(c, 0.7) for c in ["red", "green", "blue"]],)(np.linspace(0, 1, len(re)))
        airfoil_name = file.split(".")[0]
        print(airfoil_name)
        # print(Aero)

        # Saving Analysis results to CSV
        df = pd.DataFrame({
            "airfoil_path": af.name,
            "airfoil_name": airfoil_name,
            "alpha_deg": Alpha.flatten(),
            "Re": Re.flatten(),
            "Velocity": velocity,
            "CL": res["CL"],
            "CD": res["CD"],
            "CL/CD": res["CL"] / res["CD"],
            "CM": res["CM"],
        })
        df.to_csv(
            output_file,
            mode="a",
            header=not os.path.exists(output_file),
            index=False,
        )
        print(f"Saved analysis results of {airfoil_name} in {output_file}")


db = pd.read_csv("neuralfoil_output.csv")

# # Plotting a Graph for particular airfoil
# airfoil_to_plot = "123456"
# af_plot = db[db["airfoil_name"] == airfoil_to_plot]

# # Plotting a Graph Alpha vs CL for particular airfoil
# fig, ax = plt.subplots()
# if airfoil_to_plot in af_plot["airfoil_name"].values:
#     for Re_val in sorted(af_plot["Re"].unique()):
#         d = af_plot[af_plot["Re"] == Re_val]
#         ax.plot(
#         d["alpha_deg"],
#         d["CL"],
#         label=f"Re = {eng_string(Re_val)}",
#     )
#     ax.set_title("$C_L$ vs $\\alpha$ of Airfoil " + airfoil_to_plot)
#     ax.set_xlabel("Angle of attack $\\alpha$")
#     ax.set_ylabel("Lift coefficient $C_L$")
#     ax.legend()
#     ax.grid(True)

# else:
#     print(f"Airfoil '{airfoil_to_plot}' not found in the database.")

# # Plotting a Graph Alpha vs CD for particular airfoil
# fig, ax = plt.subplots()
# if airfoil_to_plot in af_plot["airfoil_name"].values:
#     for Re_val in sorted(af_plot["Re"].unique()):
#         d = af_plot[af_plot["Re"] == Re_val]
#         ax.plot(
#             d["alpha_deg"],
#             d["CD"],
#             label=f"Re = {eng_string(Re_val)}",
#         )
#     ax.set_title("$C_D$ vs $\\alpha$ of Airfoil " + airfoil_to_plot)
#     ax.set_xlabel("Angle of attack $\\alpha$")
#     ax.set_ylabel("Drag coefficient $C_D$")
#     ax.legend()
#     ax.grid(True)
# else:
#     print(f"Airfoil '{airfoil_to_plot}' not found in the database.")

# # Plotting a Graph CL vs CD for particular airfoil
# fig, ax = plt.subplots()
# if airfoil_to_plot in af_plot["airfoil_name"].values:
#     for Re_val in sorted(af_plot["Re"].unique()):
#         d = af_plot[af_plot["Re"] == Re_val]
#         ax.plot(
#             d["CD"],
#             d["CL"],
#             label=f"Re = {eng_string(Re_val)}",
#         )
#     ax.set_title("$C_L$ vs $C_D$ of Airfoil " + airfoil_to_plot)
#     ax.set_xlabel("Drag coefficient $C_D$")
#     ax.set_ylabel("Lift coefficient $C_L$")
#     ax.legend()
#     ax.grid(True)
# else:
#     print(f"Airfoil '{airfoil_to_plot}' not found in the database.")

# # Plotting a Graph Alpha vs CL/CD for particular airfoil
# fig, ax = plt.subplots()
# if airfoil_to_plot in af_plot["airfoil_name"].values:
#     for Re_val in sorted(af_plot["Re"].unique()):
#         d = af_plot[af_plot["Re"] == Re_val]
#         ax.plot(
#             d["alpha_deg"],
#             d["CL/CD"],
#             label=f"Re = {eng_string(Re_val)}",
#         )
#     ax.set_title("$C_L/C_D$ vs $\\alpha$ of Airfoil " + airfoil_to_plot)
#     ax.set_xlabel("Angle of attack $\\alpha$")
#     ax.set_ylabel("Lift-to-drag ratio $C_L/C_D$")
#     ax.legend()
#     ax.grid(True)
# else:
#     print(f"Airfoil '{airfoil_to_plot}' not found in the database.")

# # Plotting a Graph Alpha vs CM for particular airfoil
# fig, ax = plt.subplots()
# if airfoil_to_plot in af_plot["airfoil_name"].values:
#     for Re_val in sorted(af_plot["Re"].unique()):
#         d = af_plot[af_plot["Re"] == Re_val]
#         ax.plot(d["alpha_deg"], d["CM"], label=f"Re = {eng_string(Re_val)}")
#     ax.set_title("$C_M$ vs $\\alpha$ of Airfoil " + airfoil_to_plot)
#     ax.set_xlabel("Angle of attack $\\alpha$")
#     ax.set_ylabel("Moment coefficient $C_M$")
#     ax.legend()
#     ax.grid(True)
# else:
#     print(f"Airfoil '{airfoil_to_plot}' not found in the database.")


# Plotting a Graph for multiple airfoils at particular Re
# Re_target = 3.5e5
# airfoils = ["123456", "ag03", "s1223"]

# # Plotting a Graph CL vs alpha for multiple airfoils at particular Re
# fig, ax = plt.subplots()
# for af in airfoils:
#     d = db[(db["airfoil_name"] == af) & (np.isclose(db["Re"], Re_target, rtol=1e-4))]
#     ax.plot(d["alpha_deg"], d["CL"], label=af)

# ax.set_title(f"$C_L$–$\\alpha$ at Re={eng_string(Re_target)}")
# ax.set_xlabel("Angle of attack $\\alpha$")
# ax.set_ylabel("$C_L$")
# ax.legend()
# ax.grid(True)

# # Plotting a Graph CD vs alpha for multiple airfoils at particular Re
# fig, ax = plt.subplots()
# for af in airfoils:
#     d = db[(db["airfoil_name"] == af) & (np.isclose(db["Re"], Re_target, rtol=1e-4))]
#     ax.plot(d["alpha_deg"], d["CD"], label=af)

# ax.set_title(f"$C_D$–$\\alpha$ at Re={eng_string(Re_target)}")
# ax.set_xlabel("Angle of attack $\\alpha$")
# ax.set_ylabel("$C_D$")
# ax.legend()
# ax.grid(True)

# # Plotting a Graph CL vs CD for multiple airfoils at particular Re
# fig, ax = plt.subplots()
# for af in airfoils:
#     d = db[(db["airfoil_name"] == af) & (np.isclose(db["Re"], Re_target, rtol=1e-4))]
#     ax.plot(d["CD"], d["CL"], label=af)

# ax.set_title(f"$C_L$–$C_D$ at Re={eng_string(Re_target)}")
# ax.set_xlabel("$C_D$")
# ax.set_ylabel("$C_L$")
# ax.legend()
# ax.grid(True)

# Plotting a Graph CL/CD vs alpha for multiple airfoils at particular Re
# fig, ax = plt.subplots()
# for af in airfoils:
#     d = db[(db["airfoil_name"] == af) & (np.isclose(db["Re"], Re_target, rtol=1e-4))]
#     ax.plot(d["alpha_deg"], d["CL/CD"], label=af)

# ax.set_title(f"$C_L/C_D$–$\\alpha$ at Re={eng_string(Re_target)}")
# ax.set_xlabel("Angle of attack $\\alpha$")
# ax.set_ylabel("$C_L/C_D$")
# ax.legend()
# ax.grid(True)

# Plotting a Graph CM vs alpha for multiple airfoils at particular Re
# fig, ax = plt.subplots()
# for af in airfoils:
#     d = db[(db["airfoil_name"] == af) & (np.isclose(db["Re"], Re_target, rtol=1e-4))]
#     ax.plot(d["alpha_deg"], d["CM"], label=af)

# ax.set_title(f"$C_M$–$\\alpha$ at Re={eng_string(Re_target)}")
# ax.set_xlabel("Angle of attack $\\alpha$")
# ax.set_ylabel("$C_M$")
# ax.legend()
# ax.grid(True)

# plt.show()
         


stall_data = (
    db.loc[db.groupby(["airfoil_name", "Re"])["CL"].idxmax()]
    [["airfoil_name", "Re", "alpha_deg", "CL"]].rename(columns={"alpha_deg": "stall_angle_deg","CL": "CL_max"})
)

df_oper = db[(db["alpha_deg"] >= 0) & (db["alpha_deg"] <= 5)]


mean_oper = (
    df_oper.loc[df_oper.groupby(["airfoil_name", "Re"])["CL/CD"].idxmax()]
    [["airfoil_name", "alpha_deg", "Re", "Velocity","CL","CD","CL/CD"]].rename(columns={"alpha_deg": "Optimum_angle","CL": "Optimum_CL","CD":"Optimum_CD","CL/CD":"MAX_CL/CD"})
)



Zero_oper = db[db["alpha_deg"] == 0.0][["airfoil_name","Re","CL","CD"]].rename(columns={"CL":"CL_at_0_deg","CD":"CD_at_0_deg"})


final_df = mean_oper.merge(
    stall_data,
    on=["airfoil_name", "Re"],
    how="left"
).merge(
    Zero_oper,
    on=["airfoil_name", "Re"],
    how="left"
)

final_df["angle_diff"] = final_df["stall_angle_deg"] - final_df["Optimum_angle"]


def normalize(series, invert=False):
    s = series.copy()
    if invert:
        s = -s
    return (s - s.min()) / (s.max() - s.min())

scored = final_df.copy()

scored["Optimum_CL_n"]    = normalize(scored["Optimum_CL"])
scored["Optimum_CD_n"]    = normalize(scored["Optimum_CD"], invert=True)
scored["MAX_CL/CD_n"]     = normalize(scored["MAX_CL/CD"])
scored["CL_max_n"]        = normalize(scored["CL_max"])
scored["CL_at_0_deg_n"]   = normalize(scored["CL_at_0_deg"])
scored["angle_diff_n"]    = normalize(scored["angle_diff"])

# user input 
APPLICATION_WEIGHTS = {
    "payload": {
        "MAX_CL/CD_n": 0.25,
        "Optimum_CL_n": 0.30,
        "CL_max_n": 0.20,
        "CL_at_0_deg_n": 0.10,
        "angle_diff_n": 0.10,
        "Optimum_CD_n": 0.05,
    },

    "endurance": {
        "MAX_CL/CD_n": 0.40,
        "Optimum_CD_n": 0.20,
        "Optimum_CL_n": 0.15,
        "angle_diff_n": 0.15,
        "CL_at_0_deg_n": 0.10,
    },

    "trainer": {
        "angle_diff_n": 0.35,
        "CL_at_0_deg_n": 0.20,
        "CL_max_n": 0.20,
        "MAX_CL/CD_n": 0.15,
        "Optimum_CL_n": 0.10,
    }
}

def score_airfoils(df, application):
    weights = APPLICATION_WEIGHTS[application]
    df = df.copy()
    df["score"] = sum(weights[k] * df[k] for k in weights)
    return df.sort_values("score", ascending=False).reset_index(drop=True)

ranked = score_airfoils(scored, application="payload")


# Display airfoils rankwise with their details  
ranked["Suitable_chord"]=(ranked["Re"] * 1.81e-5) / (1.225 * velocity)


if os.path.exists(output_file):
    os.remove(output_file)
ranked.to_csv(output_file, index=False)



rows = []
for _, row in ranked.iterrows():
    for AR in aspect_ratios:
        wingspan = AR * row["Suitable_chord"]
        if wingspan <= Max_wingspan_limit:
            rows.append({
                "airfoil_name": row["airfoil_name"],
                "Re": row["Re"],
                "Suitable_chord": row["Suitable_chord"],
                "Aspect_Ratio": AR,
                "Wingspan_m": wingspan,
                "velocity": velocity,
                "Optimum_angle": row["Optimum_angle"],
                "Optimum_CL": row["Optimum_CL"],
                "Optimum_CD": row["Optimum_CD"],
                "MAX_CL/CD": row["MAX_CL/CD"],
                "CL_max": row["CL_max"],
                "CL_at_0_deg": row["CL_at_0_deg"],
                "stall_angle_deg": row["stall_angle_deg"],
                "angle_diff": row["angle_diff"],
                "score": row["score"],
            })

final_wing_df = pd.DataFrame(rows)

if os.path.exists("final_wing_data.csv"):
    os.remove("final_wing_data.csv")
final_wing_df.to_csv("final_wing_data.csv", index=False)
print("Saved final wing design data in final_wing_data.csv")


# Wing analysis of the airfoil 
def wing_analysis(airfoil_name, chord, wingspan, velocity, alpha):
    airfoil_path = os.path.join(folder, airfoil_name + ".dat")
    print(airfoil_path,"analysis started")
    wing_airfoil = asb.Airfoil(airfoil_path)
    airplane = asb.Airplane(
        name="AEROCLUB_NITTE_RC_PLANE",
        xyz_ref=[0, 2, 0],  # CG location
        wings=[
            asb.Wing(
                name="Rectangular Wing",
                symmetric=True,  # Should this wing be mirrored across the XZ plane?
                xsecs=[  # The wing's cross ("X") sections
                    asb.WingXSec(  # Root
                        xyz_le=[0,0,0],  # Coordinates of the XSec's leading edge, relative to the wing's leading edge.
                        chord=chord,
                        twist=0,  # degrees
                        airfoil=wing_airfoil),
                    asb.WingXSec(
                        xyz_le=[0, wingspan / 2, 0],
                        chord=chord,
                        twist=0,
                        airfoil=wing_airfoil)],
            )],)
    vlm = asb.VortexLatticeMethod(
        airplane=airplane,
            op_point=asb.OperatingPoint(
            velocity=velocity,  # m/s
            alpha=alpha,  # degree
            ),)
    aero = vlm.run()  # Returns a dictionary
    # Optionally display the geometry
    vlm.draw(show_kwargs=dict(jupyter_backend="static"))
    return aero

wing_results = []
for _, row in final_wing_df.iterrows():
    wing_para = wing_analysis(
        airfoil_name=row["airfoil_name"],
        chord=row["Suitable_chord"],
        wingspan=row["Wingspan_m"],
        velocity=row["velocity"],
        alpha=row["Optimum_angle"],
    )
    # Add the row data along with wing analysis results
    result_row = row.to_dict()
    result_row.update(wing_para)
    wing_results.append(result_row)

wing_para_df = pd.DataFrame(wing_results)

if os.path.exists("final_wing_data.csv"):
    os.remove("final_wing_data.csv")
wing_para_df.to_csv("final_wing_data.csv", index=False)
print("Saved final wing design data in final_wing_data.csv")


suitable_wings = []
for _, row in wing_para_df.iterrows():
    lift= row["CL"]*0.5*1.225*velocity**2*row["Suitable_chord"]*row["Wingspan_m"]
    if lift>=MTOW_newtons:
        suitable_wings.append({
            "airfoil_name": row["airfoil_name"],
            "Re": row["Re"],
            "Aspect_Ratio": row["Aspect_Ratio"],
            "Suitable_chord": row["Suitable_chord"],
            "Wingspan_m": row["Wingspan_m"],
            "Lift_Kgs": lift/9.81,
        })

# After the loop, rank and print
suitable_wings_df = pd.DataFrame(suitable_wings)
suitable_wings_df["Lift_norm"] = normalize(suitable_wings_df["Lift_Kgs"])
suitable_wings_df["Span_norm"] = normalize(suitable_wings_df["Wingspan_m"])
suitable_wings_df["final_score"] = 0.5 * suitable_wings_df["Lift_norm"] + 0.5 * suitable_wings_df["Span_norm"]
suitable_wings_df = suitable_wings_df.sort_values("final_score", ascending=False).reset_index(drop=True)

print("\nRanked airfoils meeting MTOW requirement:")
print(suitable_wings_df[["airfoil_name", "Re", "Aspect_Ratio", "Suitable_chord", "Wingspan_m", "Lift_Kgs", "final_score"]])

