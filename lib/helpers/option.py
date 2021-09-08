from discord_slash.utils.manage_commands import create_option, create_choice
from lib.db import DB

# option types: https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-type

class OptionMaker:
    @staticmethod
    def raid_info_options():
        """
        레이드 정보 선택을 위한 옵션을 반환
        :return: [create_option()]
        """
        choices = [create_choice(
            name="현재",
            value="현재"
        )]
        for boss in DB.get_raid_bosses():
            choices.append(create_choice(
                name=boss,
                value=boss
            ))

        option = create_option(
            name="boss",
            description="어떤 레이드 보스를 알려드릴까요?",
            required=True,
            option_type=3,
            choices=choices
        )

        return [option]

    @staticmethod
    def today_effect_options():
        """
        오늘의 혜택 선택을 위한 옵션 반환
        :return: [create_option()]
        """
        choices = [
            create_choice(name="오늘", value=-1),
            create_choice(name="월요일", value=0),
            create_choice(name="화요일", value=1),
            create_choice(name="수요일", value=2),
            create_choice(name="목요일", value=3),
            create_choice(name="금요일", value=4),
            create_choice(name="토요일", value=5),
            create_choice(name="일요일", value=6)
        ]
        options = [
            create_option(
                name="which",
                description="어떤 것이 궁금하세요?",
                required=True,
                option_type=3,
                choices=[
                    create_choice(name="요일효과", value="요일"),
                    create_choice(name="어드밴스드 상세", value="어드밴스드"),
                ]
            ),
            create_option(
                name="day",
                description="무슨 요일을 알려드릴까요?",
                required=True,
                option_type=4,
                choices=choices
            )
        ]

        return options
