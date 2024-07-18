def adapt_device_name(name, supports_multiple_batteries):
    if supports_multiple_batteries:
        return [f"{name}B{i}" for i in range(1, 6)]
    else:
        special_devices = {
            "Kadri": "Kadri_K2",
            "Kolkhozchien": "Kolkhozchien_K",
            "Gulbuta-Center": "Gulbuta-Center_K2",
            "XojaXabib": "XojaXabib_xh",
            "Hisor-Iston1": "Hisor-Iston1_h1",
            "Hisor-Iston2": "Hisor-Iston2_h2",
            "Kushtepa": "Kushtepa_K2",
            "Avtorinok": "Avtorinok_K2",
            "Pticeferma": "Pticeferma_K2",
            "Moyka": "Moyka_K2",
            "Mkr-53": "Mkr-53_K2",
            "Pedinstitut": "Pedinstitut_K2",
        }
        if name in special_devices:
            return [special_devices[name]]
        else:
            return [f"{name}B1"]