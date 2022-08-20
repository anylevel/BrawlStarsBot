import os


def get_token_api() -> str:
    with open("config.txt", 'r') as file:
        data = file.read()
    token = data.rstrip()
    return token


def get_token_bot() -> str:
    bot_token = os.getenv("API_TOKEN")
    if not bot_token:
        raise ValueError("Ошибка при получении токена")
    return bot_token

    # commands = ["/start", "/change", "/cancel", "/player_info"]
    # states = ["Token:waiting_for_get_token", "ClanToken:waiting_for_get_token", "ClanToken:finish_get_token"]


headers_brawl_api = {
    "Accept": "application/json",
    "authorization": f"Bearer {get_token_api()}",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:103.0) Gecko/20100101 Firefox/103.0'
}
headers_brawlify = {
    'Accept': 'text/html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:103.0) Gecko/20100101 Firefox/103.0'
}

places = {'0': "th", '1': "st", '2': "nd", '3': 'rd', '4': 'th', '5': 'fifth', '6': 'th', '7': "th", '8': "th",
          '9': "th", '10': "th"}

# TODO дозаполнить
maps = {"gemGrab": "Gem Grab", "soloShowdown": "Solo Showdown", "brawlBall": "Brawl Ball", "hotZone": "Hot Zone",
        "knockout": "Knockout", "bigGame": "Big Game", "hunters": "Hunters"}
stickers_top_players = [r'CAACAgIAAxkBAAEFkfVi-r-kGtL6Iq7sPeOk9IFl0CMoqQACJw8AAj5UgUst62DahfT24SkE',
                        r'CAACAgIAAxkBAAEFkfdi-r-oyFXMKGScDS10AlbrfFj2iAACERAAAsZ1oUtdujJ6liKARykE',
                        r'CAACAgIAAxkBAAEFkfli-r-sYJeugJYAAZPfq6-RHvrHtakAAuoMAAKidYBLMtFcifLlxSgpBA',
                        r'CAACAgIAAxkBAAEFkfti-r-voujcrgkgC4dvoTFZp1U2KgACThEAAnkSeUscyQpmwWBjAAEpBA',
                        r'CAACAgIAAxkBAAEFkf1i-r-xczWvAvxKKsRqvy91k79_VwACEhEAAuGDoUpK4nb80P_UGCkE',
                        r'CAACAgIAAxkBAAEFkf9i-r-0bPbcnsY-ST58rQ9FzCQ3VwACEhAAAhj6oEpr_t_5Y2iZHSkE',
                        r'CAACAgIAAxkBAAEFkgFi-r_d90-fUXc4OotnfV_h1YsgCQACagwAAnTNCEt2YmvpJSk7dikE',
                        r'CAACAgIAAxkBAAEFkgNi-r_hghtysNq64_TeVSYa-IBeMAACWAwAAvF-CUsWv4wpzmPG0ikE',
                        r'CAACAgIAAxkBAAEFkgVi-r_oIBne94vEggpNf3V669TqOAACBBoAAtQY2EqWHjOp_x8M1CkE']
stickers_top_clans = [r'CAACAgIAAxkBAAEFknxi-tI82kzxOqHorfMaMr1ZUzoajgACxAADw7nhMEkFxGPj2hD6KQQ',
                      r'CAACAgIAAxkBAAEFkn5i-tI-g22cisaYNv1LAAEu_6ApQz0AAsYAA8O54TB6p5PcyWybCikE',
                      r'CAACAgIAAxkBAAEFkoBi-tJA84OyvKaQSewaz3IPCgjFFAACxQADw7nhMIVlVMiGK9G0KQQ',
                      r'CAACAgIAAxkBAAEFkoJi-tJBonGdYfCcoLERPnPWnEmpfQACwQADw7nhMBlEIRYGJTCHKQQ',
                      r'CAACAgIAAxkBAAEFkoNi-tJCd-W2kg4F17PMhz2jRueMcQACwgADw7nhMNiqGatMaCMfKQQ']

sticker_trophies = [r'CAACAgIAAxkBAAEFkgdi-sDvFCnmqYI_ikVk2oAoeGo2VAACpQADw7nhMDK93z-SzMIvKQQ',
                    r'CAACAgIAAxkBAAEFkgli-sDxGhd-TbArx6NqJKUla1X9MQACrAADw7nhMMNcWFVaXpzqKQQ',
                    r'CAACAgIAAxkBAAEFkgti-sD1HmtwhC1nwJexYbY-8BkyXwACqAADw7nhMMgodXiytoN1KQQ',
                    r'CAACAgIAAxkBAAEFkgxi-sD2LEocVG0dRkr45VX3CPTS8gACqQADw7nhMFl4xwnn3W8tKQQ',
                    r'CAACAgIAAxkBAAEFkg5i-sD2JJHEtP1Pt-Ypw6k8ZY2K6wACqgADw7nhMGK-wPdi5twXKQQ',
                    r'CAACAgIAAxkBAAEFkhFi-sD4ZGbwKPxQ7NEaahImtwpdUwAC8QsAApSd-UrLGGOpFMFeHikE',
                    r'CAACAgIAAxkBAAEFkhJi-sD5zYkBLZPANlxICNE_kevEmwACdA4AAh7GUEviJXY_KNTeLykE',
                    r'CAACAgIAAxkBAAEFkhRi-sD6teI0URLg0LNMe1c0y7E9GwACqQ0AAvOw-ErioxSw0PYohCkE',
                    r'CAACAgIAAxkBAAEFkhZi-sD6lAhKdRDoD-rjw2dlnYko0AACCgwAAm8D-EoAAUcuhCSOBlgpBA',
                    r'CAACAgIAAxkBAAEFkhhi-sD8ql4M7w3K_zDh2NIp-AEn4gACQxAAAsqeUEnxT01aLvxlwCkE',
                    r'CAACAgIAAxkBAAEFkhpi-sD9qk2ZJShIs9tq932X9_BKjgACCRAAAiV0WUl2iKtp0XCCuSkE',
                    r'CAACAgIAAxkBAAEFkhti-sD-GjFfqbfqSzhcg_8wWz7muwACHBEAAlzEUUlX3oy74ZKSBSkE',
                    r'CAACAgIAAxkBAAEFkh9i-sEBnAiosAij1aBXYsOECJE69AACgBIAAgiOWEk6S9V1AAGHuIwpBA']

brawlers_dict = {"SHELLY": r'CAACAgIAAxkBAAEFi_di90xHAqUsEsYx3v_02sEGY3hxvAACWRUAAgRD0Ugm0W4hTStboCkE',
                 "COLT": r'CAACAgIAAxkBAAEFjHRi91ilTEZc2tNmIQngsjhiSKFDOgAC-hcAAvi7EUjCkqNxqNbugSkE',
                 "BULL": r'CAACAgIAAxkBAAEFi_ti900dYIAgVlBt5y0XrhVhqB8g-AACYREAAvicgUlmSsYsEEC-uykE',
                 "RICO": r'CAACAgIAAxkBAAEFi_1i90087Tl6hSsvppJ9Bs_Sf-WeagACDBYAAqNC-EgxqFkkXHfGhykE',
                 "SPIKE": r'CAACAgIAAxkBAAEFjHhi91jpaIVlsUOhEIRPToy3Fo4QUAACQRoAAiejGEiI384xBnWS4SkE',
                 "BARLEY": r'CAACAgIAAxkBAAEFjAFi902-SwABUCcQ5lNB-r_aqopmOiwAAmEYAAKUHYhIUY_LBMe4D0UpBA',
                 "JESSIE": r'CAACAgIAAxkBAAEFjANi903dGSH-HzmM8dQF4HFExMXk-wACbRcAAk96gUnctxyTCU5GqCkE',
                 "NITA": r'CAACAgIAAxkBAAEFjAVi904DpHDHbJGioqcyBExy22E-8AACThcAAmwsmEhPdRUugvPz_CkE',
                 "DYNAMIKE": r'CAACAgIAAxkBAAEFjAdi909-6WBQ0jky7L51j-67oUvohwAChxcAArlNEEgapXEB1yINHSkE',
                 "EL PRIMO": r'CAACAgIAAxkBAAEFjAli90-m7WUiYtIrWBPvYGxtOEV0owACaRwAAjwVKUl_82t2ZVvvfykE',
                 "MORTIS": r'CAACAgIAAxkBAAEFjAti90_FBSCHx56cFd9t0IgEGYS6bQAC1BYAAlonkEhLEeert_WTXikE',
                 "CROW": r'CAACAgIAAxkBAAEFjHZi91jG2Kloy8ZmBuzfU_8Gi0-C5QAC1RkAAnHRGUhKL27-de32PCkE',
                 "POCO": r'CAACAgIAAxkBAAEFjA9i91A3Ec2fxSwyXN8hfhYOLViTdAACmhgAAkFmuUknNUh4kiU-eCkE',
                 "BO": r'CAACAgIAAxkBAAEFjBFi91CCX1oVIimdFn663WkM1dE56gACSxYAAskhEUghIC1jyDdM_SkE',
                 "PIPER": r'CAACAgIAAxkBAAEFjBNi91ClYzZ4XiglShiu8Qm7a5LgnwACxRUAAqkYyUj7YrshkFtn_CkE',
                 "PAM": r'CAACAgIAAxkBAAEFjBVi91DYrG-IrbaMmdzzrTd2hEBtYAACvgoAAl2zCEuY7UEXO_7dZSkE',
                 "TARA": r'CAACAgIAAxkBAAEFjBdi91D8fMk5TjAcyQdFKe2hDryQ8wACJBcAAlqeyUi1H_UEij0w-ykE',
                 "DARRYL": r'CAACAgIAAxkBAAEFjBli91EoEW5gcW_wsPcPUagTvcdJpwACRg0AAuaKCEvOw8-3TDDrnSkE',
                 "PENNY": r'CAACAgIAAxkBAAEFjBti91FE39O5ilG1OFw-AuZK8iOZsQAC-RcAAj6joEpdsjyhmFBBdSkE',
                 "FRANK": r'CAACAgIAAxkBAAEFjB1i91FfTfRzea4JWvFrixummvacyAACLxUAAjMCyUjoKCgTTwSyIykE',
                 "GENE": r'CAACAgIAAxkBAAEFjB9i91GGoGPA8hcjEurR6qJH-n5iBgACARcAAp_40UhiQ_GOsIljgSkE',
                 "TICK": r'CAACAgIAAxkBAAEFjCFi91GflOhmtkz4AAG_rQkmPtQ8IdgAAp8TAAKwuBFJucK0bvl6PYUpBA',
                 "LEON": r'CAACAgIAAxkBAAEFjCNi91G0-jooRpQLn0jIlt3qnrObpAACyhYAArCXqUhlxfDnDDaTEikE',
                 "ROSA": r'CAACAgIAAxkBAAEFjCdi91ImIy95N3fcGSdJt8CzdVnqkwACkxUAAjU4EEiIg0psHsKsAAEpBA',
                 "CARL": r'CAACAgIAAxkBAAEFjCli91J6HSRw3-ErdP-59G5ysoH1aAACRhQAAsIdEUiYpNun_ATyMCkE',
                 "BIBI": r'CAACAgIAAxkBAAEFjCti91Ki2VR8EYIwCYt2tJP3gvTgAwACcBYAAqE8mUh-hCue0GSPXikE',
                 "8-BIT": r'CAACAgIAAxkBAAEFjC1i91K5KQgEp9zl_H-CXGS32GlYbgACBRgAAs_HCEn0yef0AykPAykE',
                 "SANDY": r'CAACAgIAAxkBAAEFjC9i91LkwY7uPkKFszjA5M0UfdIPigACPRgAAo8MgUjVXiWBE1WSBikE',
                 "BEA": r'CAACAgIAAxkBAAEFjDFi91L2FUGnVV5p1B3U5lhVbj2uNgACqRUAAjQLwEiwek2ZD_hyRikE',
                 "EMZ": r'CAACAgIAAxkBAAEFjDNi91MLELm9mCeWz8W0-Ej3A6FY3AACBRYAAj-EmUgm3l_TgNo_kCkE',
                 "MR. P": r'CAACAgIAAxkBAAEFjDVi91NPJVYZeuhQNwoTToBHgCTmcQACfxYAAp27GEgKOwycz1-PCykE',
                 "MAX": r'CAACAgIAAxkBAAEFjDdi91NsrWZaj288yCds7aOqnPavUQACbhMAArcxAAFJD3QuPWtUF-IpBA',
                 "JACKY": r'CAACAgIAAxkBAAEFjDli91OdEur6VYi7l7AnLnL30_b8YAACQRYAAm1QEUgyK9S7YINOPCkE',
                 "GALE": r'CAACAgIAAxkBAAEFjDti91P0f88RkoaOywOi33w_O_nGKAACDRgAAvygEUgTvIQbpTDkbCkE',
                 "NANI": r'CAACAgIAAxkBAAEFjD1i91RAcvDZgxJIV_UYm1Bh2CZzwwAC3hUAAjUrGEgd-y6cjBNgTikE',
                 "SPROUT": r'CAACAgIAAxkBAAEFjD9i91RiHTwbw6HPz_azqcfZdSItbQACgBQAAhFEqEgagPchSpg7sykE',
                 "SURGE": r'CAACAgIAAxkBAAEFjEFi91R85TRJBrWQJisUXFzucXpzlgACMxcAAkneAUlUUVHw39PXAAEpBA',
                 "COLETTE": r'CAACAgIAAxkBAAEFjEZi91SVj-DRKSKR6gfcOfh79zyL5AACSBYAAmwwiUgxboHxNLndbSkE',
                 "AMBER": r'CAACAgIAAxkBAAEFjExi91TSKdMhGfXhGXZEeaTpvLWkEgACIxQAAjOhEEgeIBHqy6tP6SkE',
                 "LOU": r'CAACAgIAAxkBAAEFjE5i91USUe0RVSl0k_ZpVYrL1esnsgACVhgAAlkpGUjcseaRAutY0ykE',
                 "BYRON": r'CAACAgIAAxkBAAEFjFBi91Uz5wPrnWdQWxFrrXkfKLMz4gACgRUAAiDysEiJQVrK88pXPykE',
                 "EDGAR": r'CAACAgIAAxkBAAEFjFJi91VI43debFuB4xazDO_R5gK-sAACMxUAAsa6eEjtYsS2onlvUikE',
                 "COLONEL\nRUFFS": r'CAACAgIAAxkBAAEFjFRi91WPirrbubIeuKcCUp5erd1UcAACChQAArf1GUimmxMKUHhy_CkE',
                 "STU": r'CAACAgIAAxkBAAEFjFZi91XO35hKEQMqUJjE4TUEioGIKgACeBMAAo5HGEiUV-jzPxZBeikE',
                 "BELLE": r'CAACAgIAAxkBAAEFjFhi91Xuq8uVTsSTjJ0q2DByAYx7YgACHxYAAmRBwEjMwumo6GxXvCkE',
                 "SQUEAK": r'CAACAgIAAxkBAAEFjFpi91YC2rmNsmZ1vQGRL8hTykFR9wACUhUAAtQRiUhkWJ4m7uPR-SkE',
                 "GROM": r'CAACAgIAAxkBAAEFjFxi91Y_H62bCHy0kJqKPiEJSkJh0AACJhYAAkNFGUgaB5CBgTm50CkE',
                 "BUZZ": r'CAACAgIAAxkBAAEFjF5i91ZdKqV9UgF1UHimO9rmgF1EHwAC1BQAAiRh6EgnHO_7283dNykE',
                 "GRIFF": r'CAACAgIAAxkBAAEFjGBi91aNw5yz0j6BeUH16PCZews4lgACIxMAAhC6EUheU1obiPgcYikE',
                 "ASH": r'CAACAgIAAxkBAAEFjGJi91bEQMEBrVPA16PSFAeE6vIXBwACIRgAApFLGEjp-29PllltOSkE',
                 "MEG": r'CAACAgIAAxkBAAEFjGRi91b4Cnyhyp-2MlGBNRHjDvn8SwACgxcAAs28GUitMDb32yuq-CkE',
                 "LOLA": r'CAACAgIAAxkBAAEFjGZi91cXuQlxZjfdOqOfjaqXz8qsEwACRBcAAgTr6UgAAU0bF4txbVMpBA',
                 "FANG": r'CAACAgIAAxkBAAEFjGxi91em-GFB2rRtxfLu3ICfujTdRQACAxYAAmUugEjBsXtkMHRmMykE',
                 "EVE": r'CAACAgIAAxkBAAEFjGpi91eEgBs7bY9q2GGacPgv45huqQACFhsAArAbEUlXr4UttZ_1QSkE',
                 "JANET": r'CAACAgIAAxkBAAEFjG5i91gMkAQ4BsVWzZoNuVzrklAXhQACohcAAnZiAUgpBDaugigMfykE',
                 "BONNIE": r'CAACAgIAAxkBAAEFjHBi91g4gC0BYFWMAtEa5mqVNzpw_AACYR0AAmeF-UuCEqX6uOa7MCkE',
                 "OTIS": r'CAACAgIAAxkBAAEFjHJi91hdJWq1Av0WW-4mFNj_P-CnggACuxoAAg43OUpDZmyEfgOO1ykE'
                 }
