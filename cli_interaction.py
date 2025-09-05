import sqlite3
from database_class import Database
from rawg_api_class import RawgAPI
from game_class import Game


def search_and_save_flow(rawg_client, db):
    search_term = input("\nDigite o nome do jogo que você quer buscar: ")
    if not search_term:
        print("Nenhum termo de busca inserido.")
        return
    api_results = rawg_client.search_game(search_term)
    if not api_results or not api_results.get("results"):
        print(f"Nenhum jogo encontrado para '{search_term}'.")
        return
    games_list = [Game(data) for data in api_results["results"]]
    print("\nResultados da busca:")
    for index, game in enumerate(games_list):
        print(f"[{index + 1}] - {game.name} (Lançamento: {game.released})")
    while True:
        try:
            choice_str = input(
                "\nDigite o número do jogo para salvar (ou '0' para voltar): ")
            choice_int = int(choice_str)
            if choice_int == 0:
                break
            if 1 <= choice_int <= len(games_list):
                chosen_game_summary = games_list[choice_int - 1]
                print(
                    f"\nBuscando detalhes completos para '{chosen_game_summary.name}'...")
                game_details_data = rawg_client.full_game_details(
                    chosen_game_summary.id)
                if not game_details_data:
                    print(
                        "Não foi possível obter os detalhes do jogo. Tente novamente.")
                    return
                full_detail_game = Game(game_details_data)
                print(f"\nDetalhes obtidos para '{full_detail_game.name}':")
                db.add_game(full_detail_game.to_dict())
                print(f"\n✅ Jogo '{full_detail_game.name}' salvo com sucesso!")
                break
            else:
                print("❗️ Número inválido. Por favor, escolha um número da lista.")
        except ValueError:
            print("❗️ Entrada inválida. Por favor, digite apenas um número.")


def list_saved_games_flow(db):
    saved_games = db.list_all_games()
    if not saved_games:
        print("\nVocê ainda não tem jogos salvos na sua coleção.")
        return
    print("\n--- Sua Coleção de Jogos ---")
    for game in saved_games:
        print(f"\nID: {game[0]}")
        print(f"Título: {game[1]}")
        print(f"Lançamento: {game[2]}")
        print(f"Desenvolvedores: {game[4]}")
        print(f"Publicadoras: {game[5]}")
        print(f"Gêneros: {game[6]}")
        description = game[3]
        print(f"Descrição: {description[:200]}..." if description else "N/A")
        print("----------------------------")


def delete_game_flow(db):
    saved_games = db.list_all_games()
    if not saved_games:
        print("\nVocê não tem jogos salvos para apagar.")
        return
    print("\n--- Escolha um jogo para apagar ---")
    for index, game in enumerate(saved_games):
        print(f"[{index + 1}] - {game[1]}")
    print("-----------------------------------")
    while True:
        try:
            choice_str = input(
                "\nDigite o número do jogo para apagar (ou '0' para voltar): ")
            choice_int = int(choice_str)
            if choice_int == 0:
                break
            if 1 <= choice_int <= len(saved_games):
                chosen_game = saved_games[choice_int - 1]
                game_id_to_delete = chosen_game[0]
                game_name = chosen_game[1]
                confirm = input(
                    f"Tem certeza que deseja apagar '{game_name}'? (s/n): ").lower()
                if confirm == 's':
                    db.delete_game(game_id_to_delete)
                    print(f"\n✅ Jogo '{game_name}' apagado com sucesso!")
                else:
                    print("Operação cancelada.")
                break
            else:
                print("❗️ Número inválido.")
        except ValueError:
            print("❗️ Entrada inválida. Digite apenas um número.")


def main():
    try:
        db = Database()
        rawg_client = RawgAPI()
        while True:
            print("\n===== GameLog Menu =====")
            print("[1] Buscar e salvar um novo jogo")
            print("[2] Listar jogos salvos")
            print("[3] Apagar um jogo salvo")
            print("[4] Sair")
            choice = input("Escolha uma opção: ")
            if choice == '1':
                search_and_save_flow(rawg_client, db)
            elif choice == '2':
                list_saved_games_flow(db)
            elif choice == '3':
                delete_game_flow(db)
            elif choice == '4':
                print("Obrigado por usar o GameLog! Até mais.")
                break
            else:
                print("❗️ Opção inválida. Por favor, tente novamente.")
    except (ValueError, sqlite3.Error) as e:
        print(f"\nOcorreu um erro crítico: {e}")


if __name__ == '__main__':
    main()
