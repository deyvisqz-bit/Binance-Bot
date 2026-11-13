
from src.binance_client import create_public_client
from src.market_pipeline import run_market_pipeline


def main():
    print("=" * 60)
    print("DIAGNÓSTICO COMPLETO DEL PIPELINE")
    print("=" * 60)

    try:
        client = create_public_client()

        print("\nAnalizando mercado...\n")

        result = run_market_pipeline(client, max_pairs=10)

        if not result["success"]:
            print("ERROR:", result.get("error"))
            return

        print(f"Pares analizados: {result['pairs_analyzed']}")
        print(f"Entradas encontradas: {result['entries_found']}")
        print(f"Pares en espera: {result['waiting']}")

        print("\nDETALLE POR PAR")
        print("=" * 60)

        for item in result["results"]:
            print(f"\nPAR: {item['symbol']}")
            print(f"DECISIÓN: {item['decision']}")
            print(f"DIRECCIÓN: {item['direction']}")
            print(f"PRECIO: {item['price']}")
            print(f"MOTIVO: {item['reason']}")

            print("\nTENDENCIAS:")

            for timeframe in ("15m", "5m", "1m"):
                analysis = item.get(f"trend_{timeframe}")

                if analysis:
                    print(
                        f"{timeframe}: "
                        f"{analysis.get('direction', 'N/A')}"
                    )
                else:
                    print(f"{timeframe}: SIN DATOS")

            trigger = item.get("trigger")

            if trigger:
                print("\nTRIGGER:")
                print(f"Activo: {trigger.get('trigger')}")
                print(f"Dirección: {trigger.get('direction')}")
                print(f"Motivo: {trigger.get('reason')}")

            position = item.get("range_position")

            if position:
                print("\nPOSICIÓN EN EL RANGO:")
                print(
                    f"Porcentaje: "
                    f"{position.get('position_percent'):.2f}%"
                )
                print(f"Zona: {position.get('zone')}")

        print("\n" + "=" * 60)
        print("FIN DEL DIAGNÓSTICO")
        print("=" * 60)

    except Exception as error:
        print("\nERROR EN LA PRUEBA:")
        print(error)


if __name__ == "__main__":
    main()
