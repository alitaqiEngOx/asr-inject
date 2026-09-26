""" Licensed under the same terms as described in the main 
licensing script of this repository. """

            # average diffusion coefficients
            #water_concentration_mean = np.mean([
            #    water_concentration_fresh,
            #    water_concentration_saline
            #])

            #solute_concentration_mean = np.mean([
            #    solute_concentration_fresh,
            #    solute_concentration_saline
            #])

            #water_diffusion_coefficient_average = (
            #    self.diffusivity_water *
            #    water_concentration_mean / (
            #        R * self.temperature
            #    )
            #)

            #solute_diffusion_coefficient_average = (
            #    self.diffusivity_solute *
            #    solute_concentration_mean / (
            #        R * self.temperature
            #    )
            #)

            # chemical potentials
            #water_potential_fresh = (
            #    chemical_potential.compute(
            #        activity=water_fraction_fresh,
            #        temperature=self.temperature
            #    )
            #)

            #water_potential_saline = (
            #    chemical_potential.compute(
            #        activity=water_fraction_saline,
            #        temperature=self.temperature
            #    )
            #)

            #solute_potential_fresh = (
            #    chemical_potential.compute(
            #        activity=solute_fraction_fresh,
            #        temperature=self.temperature
            #    )
            #)

            #solute_potential_saline = (
            #    chemical_potential.compute(
            #        activity=solute_fraction_saline,
            #        temperature=self.temperature
            #    )
            #)

            # fluxes
            #self.recovery_gate *= (
            #    np.heaviside(
            #        water_moles[0] + solute_moles[0] - 0.01, 0.
            #    )
            #)

            #J_w_sf = (
            #    -1. *
            #    water_diffusion_coefficient_average *
            #    self.cs_area * (
            #        (
            #            water_potential_saline -
            #            water_potential_fresh
            #        ) / self.numerical_separation
            #    )
            #)

            #J_s_sf = (
            #    -1. *
            #    solute_diffusion_coefficient_average *
            #    self.cs_area * (
            #        (
            #            solute_potential_saline -
            #            solute_potential_fresh
            #        ) / self.numerical_separation
            #    )
            #)

            #J_w_fr = (
            #    -1. *
            #    np.heaviside(
            #        (
            #            water_mass_fraction_fresh -
            #            (1. - self.max_solute_fraction)
            #        ), 0.
            #    ) *
            #    self.recovery_gate *
            #    self.recovery_rate *
            #    water_mass_fraction_fresh /
            #    self.Mr_water
            #)

            #J_s_fr = (
            #    -1. *
            #    np.heaviside(
            #        (
            #            self.max_solute_fraction -
            #            solute_mass_fraction_fresh
            #        ), 0.
            #    ) *
            #    self.recovery_gate *
            #    self.recovery_rate *
            #    solute_mass_fraction_fresh /
            #    self.Mr_solute
            #)

            #return np.asarray([
            #    -J_w_sf + J_w_fr, J_w_sf, -J_w_fr,
            #    -J_s_sf + J_s_fr, J_s_sf, -J_s_fr
            #])

        # initial condition
        #initial_moles = np.asarray([
        #    self.moles_water_fresh_initial,
        #    self.moles_water_saline_initial,
        #    0.,
        #    self.moles_solute_fresh_initial,
        #    self.moles_solute_saline_initial,
        #    0.
        #])

        # numerical solution
        #result = odeint(
        #    differential, initial_moles,
        #    np.arange(n_steps) * step_size,
        #    hmax=(
        #        hmax if hmax else 0
        #    )
        #)

        #mass_fraction_solute_fresh = (
        #    (result[:, 3] * self.Mr_solute)
        #) / (
        #    (result[:, 0] * self.Mr_water) +
        #    (result[:, 3] * self.Mr_solute)
        #)

        #efficiency = (
        #    (
        #        result[:, 2] * self.Mr_water +
        #        result[:, -1] * self.Mr_solute
        #    ) / self.density_pure
        #) / self.volume_fresh

        #if (
        #    np.max(mass_fraction_solute_fresh) <
        #    self.max_solute_fraction
        #):
            #time_at_limit = None

            #idx = 0
            #while (
            #    efficiency[-1] - efficiency[idx]
            #    >= 0.0001
            #):
            #    idx += 1

            #time_to_full_recovery = (
            #    np.arange(n_steps) * step_size
            #)[idx]

        #else:
        #    time_at_limit = np.interp(
        #        self.max_solute_fraction,
        #        mass_fraction_solute_fresh,
        #        np.arange(n_steps) * step_size,
        #    )

        #    time_to_full_recovery = None

        #return {
        #    "moles": result,
        #    "mass_fraction_solute_fresh": (
        #        mass_fraction_solute_fresh
        #    ),
        #    "asr_efficiency": efficiency,
        #    "time_to_recovery_limit": time_at_limit,
        #    "time_to_full_recovery": (
        #        time_to_full_recovery
        #    )
        #}

        #self.length = config[
        #    "reservoir_dimensions"
        #]["length"]

        #self.width = config[
        #    "reservoir_dimensions"
        #]["width"]

        #self.height = config[
        #    "reservoir_dimensions"
        #]["height"]

        #self.interlayer_thickness = config[
        #    "reservoir_dimensions"
        #]["interlayer_thickness"]

        #self.volume_fraction_fresh = config[
        #    "fresh_segment"
        #]["volume_fraction"]

                #self.mass_fraction_solute_fresh_initial = config[
        #    "fresh_segment"
        #]["solute_mass_fraction"]

        #self.mass_fraction_solute_saline_initial = config[
        #    "saline_segment"
        #]["solute_mass_fraction"]

        #self.recovery_rate = config[
        #    "recovery"
        #]["flow_rate"]

        #self.max_solute_fraction = config[
        #    "recovery"
        #]["threshold_solute_mass_fraction"]

        #self.recovery_gate = 1.

    #@property
    #def volume_fraction_saline(self) -> float:
    #    """
    #    """
    #    return 1. - self.volume_fraction_fresh


    # water moles
    #water_mass = results["moles"][:, :3] * (
    #    fitting["solution_characteristics"]["Mr_water"] /
    #    k_TO_SI
    #)

    #plt.plot(
    #    (
    #        np.arange(config["n_steps"]) *
    #        config["step_size"] / DAY_TO_SEC
    #    ),
    #    water_mass[:, 0],
    #    label="fresh segment"
    #)

    #plt.plot(
    #    (
    #        np.arange(config["n_steps"]) *
    #        config["step_size"] / DAY_TO_SEC
    #    ),
    #    water_mass[:, 1],
    #    label="intermediate segment"
    #)

    #plt.plot(
    #    (
    #        np.arange(config["n_steps"]) *
    #        config["step_size"] / DAY_TO_SEC
    #    ),
    #    water_mass[:, 2],
    #    label="saline segment"
    #)

    #time = max(
    #    results["times_to_steady_state"]["water"]
    #) / DAY_TO_SEC

    #plt.plot(
    #    np.asarray([time, time]),
    #    np.asarray([
    #        np.min(water_mass), np.max(water_mass)
    #    ]),
    #    "k--",
    #    label="time to steady state"
    #)

    #filename = "water_mass"
    #plt.legend(loc="best")
    #plt.title(outname.stem)
    #plt.xlabel("time (days)")
    #plt.ylabel("mass (kg)")
    #plt.savefig(outname.name)
    #plt.close()

    # solute moles
    #solute_mass = results["moles"][:, 3:] * (
    #    fitting["solution_characteristics"]["Mr_solute"] /
    #    k_TO_SI
    #)

    #plt.plot(
    #    (
    #        np.arange(config["n_steps"]) *
    #        config["step_size"] / DAY_TO_SEC
    #    ),
    #    solute_mass[:, 0],
    #    label="fresh segment"
    #)

    #plt.plot(
    #    (
    #        np.arange(config["n_steps"]) *
    #        config["step_size"] / DAY_TO_SEC
    #    ),
    #    solute_mass[:, 1],
    #    label="intermediate segment"
    #)

    #plt.plot(
    #    (
    #        np.arange(config["n_steps"]) *
    #        config["step_size"] / DAY_TO_SEC
    #    ),
    #    solute_mass[:, 2],
    #    label="saline segment"
    #)

    #time = max(
    #    results["times_to_steady_state"]["solute"]
    #) / DAY_TO_SEC

    #plt.plot(
    #    np.asarray([time, time]),
    #    np.asarray([
    #        np.min(solute_mass), np.max(solute_mass)
    #    ]),
    #    "k--",
    #    label="time to steady state"
    #)

    #filename = "solute_mass"
    #plt.legend(loc="best")
    #plt.title(filename)
    #plt.xlabel("time (days)")
    #plt.ylabel("mass (kg)")
    #plt.savefig(f"{outdir / f"{filename}.png"}")
    #plt.close()

    #if results["time_to_recovery_limit"]:
    #    limiting = (
    #        results["time_to_recovery_limit"] / DAY_TO_SEC
    #    )
    #    limit_label = "recovery limit"

    #else:
    #    limiting = (
    #        results["time_to_full_recovery"] / DAY_TO_SEC
    #    )
    #    limit_label = "full recovery"

    #plt.plot(
    #    (
    #        np.arange(config["n_steps"]) *
    #        config["step_size"] / DAY_TO_SEC
    #    ),
    #    water_mass[:, 2],
    #    label="recovered"
    #)

    #plt.plot(
    #    (
    #        np.arange(config["n_steps"]) *
    #        config["step_size"] / DAY_TO_SEC
    #    ),
    #    solute_mass[:, 2],
    #    label="recovered"
    #)

    #plt.plot(
    #    np.asarray([limiting, limiting]),
    #    np.asarray([
    #        np.min(solute_mass), np.max(solute_mass)
    #    ]),
    #    "k--",
    #    label=limit_label
    #)

    # mass fraction of fresh segment
    #mass_fraction = results["mass_fraction_solute_fresh"]
    #plt.plot(
    #    (
    #        np.arange(config["n_steps"]) *
    #        config["step_size"] / DAY_TO_SEC
    #    ),
    #    mass_fraction
    #)

    #plt.plot(
    #    np.asarray([limiting, limiting]),
    #    np.asarray([
    #        mass_fraction[0], mass_fraction[-1]
    #    ]),
    #    "k--",
    #    label=limit_label
    #)

    #if results["time_to_recovery_limit"]:
    #    plt.plot(
    #            np.arange(config["n_steps"]) *
    #        (
    #            config["step_size"] / DAY_TO_SEC
    #        ),
    #        (
    #            np.zeros(config["n_steps"]) +
    #            config["recovery"][
    #                "threshold_solute_mass_fraction"
    #            ]
    #        ),
    #        "k--"
    #    )

    #filename = "recovery_purity"

    #plt.legend(loc="best")
    #plt.title(filename)
    #plt.xlabel("time (days)")
    #plt.ylabel("solute mass fraction in fresh segment")
    #plt.savefig(f"{outdir / f"{filename}.png"}")
    #plt.close()

    # asr efficiency
    #plt.plot(
    #    (
    #        np.arange(config["n_steps"]) *
    #        config["step_size"] / DAY_TO_SEC
    #    ),
    #    results["asr_efficiency"] * 100.
    #)

    #plt.plot(
    #    np.asarray([limiting, limiting]),
    #    np.asarray([0., 100.]),
    #    "k--",
    #    label=limit_label
    #)

    #filename = "asr_efficiency"

    #plt.legend(loc="best")
    #plt.title(filename)
    #plt.xlabel("time (days)")
    #plt.ylabel("efficiency (%)")
    #plt.ylim(-5., 105.)
    #plt.savefig(f"{outdir / f"{filename}.png"}")
    #plt.close()