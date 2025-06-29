import asyncio
import hashlib

from pytoniq import StateInit, Contract, LiteBalancer, WalletV4R2
from pytoniq_core import HashMap, begin_cell, Builder, Address
from codes import *
from schemes import JettonMinterData, JettonWalletData
from secret import mnemo


def get_metadata():

    def key_serializer(key: str):
        return int.from_bytes(hashlib.sha256(key.encode()).digest(), 'big')

    def value_serializer(src: str, dest: Builder):
        return dest.store_ref(begin_cell().store_uint(0, 8).store_snake_string(src).end_cell())

    hm = HashMap(256, key_serializer=key_serializer, value_serializer=value_serializer)

    hm.set('name', 'Test Token')
    hm.set('description', 'Very test token')
    hm.set('symbol', 'TST')
    IMAGE = 'UklGRjwZAABXRUJQVlA4IDAZAACwagCdASrAAMAAPpE8mEiloyIhLHO9KLASCWcAzqksvmdqpqo++80LI/aV91kjDLL5X6hfsz/dem9C4099CnwH5zs9fIF4aOgL4zmkp7A9g/9heuT6SjlH/AvtoPbfre97/iXq1GFgVYlSDummGo2WGvPfRvitsefofUmpfn1///jRMH2KeP93Q00+A5UkXwZcN9sCTKZStn/JmKpE5WK8fcjmqUV0Yuvj214QzcyO0TJCQiIwab/uyYkKAh6pCQpkIYms7jvuaF6BIiPtJ2GcyBqd1cs7U/odJwbGSpeF4THbX35MwcgcvVWioXEKLB0K897o5brg1FQpiKuAi1IdwVZSv6jMCdI4gPJESULV217qY8WWkbVMGmlLPPmB0KwwtLeFjyjFAOoTLmYGwbN6oBmpevL2TDSkAJVBedL6gMbYHDroQL9rGbpmYH5AXBBGvksnPLA+6PKwh5gyZzcvWnM6gQ9FHN3z++ZbiONpEVGQv9WfheIicYzFGD1h97aSeAbcZ7tAuYcHeXReoMKZDUyrMrvzABp2Lshl6YUwRQQZper+ifl/uNLNFbJHnKq3o8WYqbOIUVsZiagb/CxOuxOGOMpf9ZIUVYZPODN6XYbysyrcu/4K3co7Zv0mOUayc/FSH0oCW/CIhXF4OZfnXSBjK5HQrEftbLEhMrusfIUt6mAPEuA4x7dwIq9tBl72zmjt9tdmkKw9F1aawvLe2V0Jv9Zs9+EfXFTsIVzZHyNROlvoa4gd03vlS8Pq/vIDRhGECFqNpfBuqRrZ5cVN1+V850UhxUG4uzHBNsM9zFNmASQkcZvd65lucd7go9ORRMWRUif1VbgANL+POsUpBd+i/hk7eJn4lc98369X+l9/AvUUjrMOwaP5hEdkOblH2ozdAolwaDmr7UYSSKVKwVKpLRW6GS6thtc/rwdVltwzNr3aAHFNRbGxTGIeroVrpYk0Psy9UsrC07TzhKYmMbQmNjivLIJodp/3cuw9PC2agTsGzQQgeOeXK5ZTcEnheC1QHGEGOJFNEmgQvoSToYGDIWT4SeuQnd+pJyDSIN5xWVB+K+Kn+73lxrc9neeTrZkgrfP+tccIy2dm/nsNYARzdHAYgX6W4Tyi6hX2h0G1GG7TzlofuxfBZvwAAP79ZT90thimXAJW+gAOj2GFg6gDRyIYA7GsQJKym0+5A8c7IMrEu81XDYp1tCUopagbe6ZvlEI73oBOnixLeT3ajeVxNXu6wCUB9lTS4yERxflcqRNT6AwQWQy9Bhfdwd9oVxcnMnUUTl9MjJoIbX7RGhM3MoHUz7LTmSuZTFTgmh82dtZnqbhrXJSNEzGXjhJIZc7EjY1nDQsS9y87LNuZ2Y3o1sUdsch6N3DAzzF0FEuYsI13EaDAJme2N+78vi2N8KfKP8BCZhj7tYYa7hJymr4tE5uAQwvqv8T/1p/gX8S4vLuU0o9/1s0HS8WA8j2K/85g+jtGPmcWDp93yq5NjJ97jG4dvYY5ZTZz0yl+Wdggo1iIX+JadjImf/IPkcPhWf6dcbAfoZO7nggIyQLyGPU/KzL8P4JAvF6EqioY9FVskmDMgwL4EpmGPsH9lpfiR1nUrv0MKE9CPr0HF296KR7iUpcVb7etJlRFLxlwS9XVY0PgFFnNg5AbTfTIZOo7Diu4syrEKeu84jMuX0dn5RYeTH/m5IkAkywzWe0mud9wHC/m79EeV0iZ0WI6HUw5/v43+QEJubNyj44DWFfX7t7NJImsQdhQ3UDHmjTx7701zrQzZ41L5GSsaKiTwxsN43F30EfAkSHuKO2YsOeygIBg5uF+l4Xfzctrk4bwy1xD0Elrqkz4NoaZx2s4jT3uKuZLUHUFMxS/SgYX3ZCn2SC0jI07fn3tFk7++Pn/JiarkUHMJe0tKf4cKlGAN3s3ohd+txPY6bAO3UfCQYmQ3oXMO7JhbyYyQ7VFrFe16FXj/m9njl9JET57ljZNHMBAmBObnYDvAiDSrcUgbwLumeZ2P6U13jCfXPn1xdkOCb0goB7jKW3VbLlKS0oowwvnB+weNAMNhW7j0zvSH/DauB+xUaoje0spK4EoAwGj1dYigUJaOmCILknw811FoPprhzSycqEXQ3/0y8opkYcpkr1a6mi8G7fE081NXKbj4N9LegLnDWgIKwy3LDXzb/lIwYyMroXlFpVUwBYH4yzpUbCUHzw4KRlczQjQq7pTZ1oswgC2HgHU0ssU/sbwAHtFPj3T9RzMu63t3z3OJtg4+z2HKiSmkVY11r4cQA13Hvh6NPdrrNoBalRYcTRHXJdq1Yv0NXuWn2lEkRnzc9BsEEU76LoN09rjbd+j1LclxEeccLPRScHLEpxaokAhTdj+fxxKQMMYTLL3MBGucsDE1uvT2eqimIbaxF5hjJGoNyxdY4xYnnvm1PjE4ND88nxol+2GfeRnLTWf2G+BdfePHU9TnkuzMmAtMYxNeQ29pa8GXIrUDGKA8bRKJcPWC702Dgz73NNHKIqG+1eUuyKJPUMjpmwthuMGy6xmW8qx8mnnndMgWW5Hv5+Pw/aiDWvrMd4YhHrXRqn+5KGMVg/8KGCRo7EoKJRvQIPA6LYmK7b5bF9z+dn+D6P3y+z9vzNjZdmao5A1oSkwdli0jhmEe0CHSgWuXo1BRbqNOh/JksX2NQs9HVQf+FpXFc++CbsMD4y+r3k6u93iNAQT+TNcMzlTFMj1lHhn3q/zlnIhzQq1wTUOEv/g5ij3JzaPcA5wOKIQdWNimXEAp2FWifxPa1HsREp2VkOQ6MQp+32nnDQXv9gH96HwW2HYzaQjTyHSyyComv0CxYQabuO1AN8FbN/gbsz6UkARCE7oCDwiN/zBcp36Blx6/XdU4D+aeyA4yi5vAY/Fpg4Q/9xyCPX/alz2dCqi6B+pMObS9XTCJ3BrOV/bzcCnNMqpVnoNCy6lUx/Oil72JxecWGwQYuc7E+ynHOluVuqFn/+uV3LQt0eHyWAE3fHStSxNkwNS3JAjwF1QsjRyptoFRIpTz7R3ymxf82Fk44E1fSxSknbfpaOL4BqPsynISVgLFMsMgXMoKJ3OfJ+MvDa4sFz5qeJ8H37dQTYNZSqF5mNkZjelqGgXOZW9gxRN0Q4sdhrwLjQexqFffhiSnpahn07aWsjoKXYZ02M8kceMQlGR70SwRJrV8aOnxrt9K8f1d28OW2lBrpuONG3ztcTZbtJ3ryOFF+M/2BvRt7Q1oAhaBNDc2zmZn/GY9zO3kLYndHjS/g/Nq/esWEJEGmRRcoQqZ12qAYQCIB3sDfXvhHHStZ05Sfj+URO/i50oSc6lrp251zhtk2nEE/c6UEt3ekfzT5CjyPFgzY2XHBG2TtWOy/dhK5RzZVbAu/2ZIwUrHGy3i5Kr4MR8zTv1FqlxshkJcQR7n0xo6LvuLsJ9XM2Af7Srt7mziWcVgxs4iOUb+gCQGbD3xH3n+X8VUFmsth72Se0nU3VLMWBhzqRhwLsZmxzcNUqqOeb7pBvSDFDl0728f/BzwK2e+nuMOJHjwfN2c0x9HUVJws2OSUhsJ/6i7eCnVYfWI0qvgKK9CkGnaHQ22BSa+YS/PYX2NvArVLO+oxvXT4TXW2Ek5nSKG0GrAx3DtOjb6iLhy6tzvyLN8GjP1MoS2uOqlee5fDcvnsupqIOBctUMtTm7I2g/X9WNhgIPoT5+j3aSrGCZGwaTXmwI0qTQyDJYtjP6waCGpTZukTpJ614qOZfnzXljPrBHv6SfFmsmBV1qJ647ARpOtUasD/g5o96B876bBJDxKdpkYZIYW6KQZdcDeffuXbiXIFdguAWDt+TYLmTIqO4tgAg1kc+AWWKYDSiG3LzkO8E01aEyZn/PaDGiKYOFyoShuEGZvgI/2DLpHN6H+yUy2zz9u4RWumyvc5XUuGJqWHmvDTyOS2/bm3+TMlw4Qknlj2bu9aW5wbrU44Ne54UCHezU/RoHzRKfb9sjlplMrVN3pUZewZ4GsN0L9H8wYUU4ux/yYxpNJo7RonjCQd2TAmU7z/NSArBmx4J270xVPIi2HdJtpp5zYdGHp4apDLg/GqkmA7SsCRszvABKYY8ToJZutxEe/2lMl4qfLv1WKmMrkQV5KIEAfdDuMdQglgxzoLa4Z/su6L2EANoQh11hsRBiRchbc/8pO1YcgMLleZV5sSjqNPPlu+GHc0Fkzkjh2u95ll8ziNHqNtFMyCYjnm+GlZfb6s0uXeS6o6e9wsyxOFYnM8iLc7PB5PBWePUFeYd9omr3JqxtK2d0co/5Q1Kpy/s14/uVHt9xgFt3CCfkT5P0mz6JvVL6Dt0pkrbmNJt1JrSbzLgxkyHWj2bROVoVU0C5yLRFoqqfYtLAvQRMV7dIys5sV7gEo8Ha7zhd6JZBJVeenrbUEriZPqbSLvjx52dLtPi8SuSnDK1sqHXKbsg1eB8NglkIgIvj55ppc4HMBfw82cupoTEjbWl3IUgSRuU+VC8lbC6nNC7WwVt/FPznw6NcJ+iOgPEg0c01fR3X+KLzqUsbQubvQo0nwUv0veIoGQk68E39VHSUO5+XTuARhFhPC9t4k3HPIqr91v6DCYmb6Xg0t3EoBLYfqZqNEhvNQ9klLjHV1EP1M/vAycPiuMwSpTS5CxUx2r7MbxJ684UAORfgqJYJWM9sIz0g1FbCzJT1DqvCpeG65L7yhxd/dDFXuuvW1LB1kRy221+AjELJUt2HJ9R1cjBmn+A4JqmJdACUMJXGsXPsh3cekfqpMMZazOF7ypKmvHVsSrZcECaOs7nMyCxDknaYx0eXQ81N5LeW/2ipNWh/wdY0nh9uHFSSrpPdVt+5OvwAu5rDhKVC9gsV/qTFAF7yfld9E7z+vqaYJoUmEwqMjLwr4+7JfMHxXuy79ytwcxta8TB5WzdKOGqtLX8zPHC3mMeqWVf3ja4lt6MAImRHyh9jHwWcbDBbP8VF723uf246QIsH2VXAs/1A+n45x222wIyoM3n1WQVXgJdULAVBp8GTowRPtiS5e14x4n+OnppPOJZWy7yxsjO3cgDkZO1G0OOwcryqZXFiD10VT7rl2pdUBWJctmMwMQ3wvv8+sSGH0J8tv8OXlGmUFJ5UyfHAjRxt4WbZ4pMRjNewGQFWMoiG5AwaITnEsEcpP6992bZzEeaKPRkDpx9ncEAfzLflxKj46bfZKmH5RsrQzpQKxhDi2Ugs5jy48XzUkWvxQzU751c4njwxd9sAO2s3IN2r8RIhkVYordS33AO5MOim4GfSK5jCpw9+vLNesPYHutxgnrx3X4+3eNsOdhWLOOkbd5df4sqHerv4t771xxsC5t5wnOJI9BO9dwGfTzzp4hwSATZ6mG0suGqNUk0ZeD9bsiSAI73UiERz4f0GOPXZfhS1WH5GOeZnVi0FuKnDx/h2RKZpis3H4WAMzQdCeId57WfCCM6APfDoNQW5bLFQAZKjaDZE7ad9V5Bmpa1JH6xEMBDERzS41n5lu+z0+3jZIGTGAqI+aqjwPLrGUNhuXO2gcfBbQrXa7BOnUbIT1FMY0ICMISN4Wwjfm61TVXexfhj+XE4MjEWskoKhUxYdgw0jn9yXOsazHoyZgIfgcZWWOouM010EV6pbZwK5qzHoONiiqZ77xYOlHiXmrs3nsVc3HidZpsIEJRQ3ITQHsX3N0UXpa9h5w4jn27PgTC07h8050C9KvcLpaXg6R1fK6Ble8jdlhE5sDMZtCElqC1g5028FkI7zthm1mf75s9W9MA0ZV9xHOFzDRzMFqcztiVtJTopd86MkjNzPONEzoDTrj6EEEvmBErKYCn759vkWYkYowixUPz4detMquRH+251w4zXlZYHbXTlNxlJbDgAjbXTcRaeYXjMYAyxI/WZCdiRZ+6eJNBfq2M/fQ4M6kbBeUttc5WLy44y+R6se7oxwmXoyOi7cVWZ/lXY3XMJaPZh0hWAy6IOvg1ii7W78kEJgrGIHUxcRzjlymd3T/Mwbef8ZBtyhvEX4g0EXjQdLCgVapzp8VwgVkt7B7QfYFLCBcIukciVTabfgyJ3Z3PePISWh2ugkpwZ0a11sqWP1HSIXzSdvzJdXuuL9+6h5ZFOiLLODm0IwuZlRFznCYtNDznoF2FFVcWW2HFYVhz0xBjAlE4Gc3aLM6oN2ICM+0mcXwHTFXfY5eq4SYiJAQw2UNUG5xgatSD7hoDVIABCQUxR4Mj29GMx2Nj+y8vG53rqSqHMR1woPchqQyUTqRi8zWv58KL7xgN+gDIjxDnLi/gxwFeIJ7Tc48Vsg60PrZMQd5xQYS3sJdimWfjlHsHUOEu3s+LWKJp66QlbssmNEMa5DREBvT1UAIDhDhr8ULtWrFLkyX5q2xhHRBP3UqZDxRpUFDTLoYb0GAS2IllFVOin3a0SwBe+B9+YO7VFvwxJGmcS5Yxum9l2AFq86xLQf6gw2otAgYIBplsnoNb1LK8WUbGSLqVpVXQl7SQPy5UBAZ+E8kGqop2RCYOxzgbmnwCfXQvYg7KXq4tAVpwdptPq3i19o8wajLYgyQfAa+m3/mmWCK8T2UfmMW5mFFBnhtJaoA7i+KFjVH7S6vWJ4d93RAPHsZoIPm1faJ57t64v/VgPrdGtfEwv6gi7xH04rhC8M7YsceJgZ1v4tX1OTXiXkhH81v8EyjAmpCaX5ieptM03WLjHwQrVtRXoTUzwAOPvsqHo0RmYQLKOkKhZC6wiZPnfpKQsKyNyon6mmLlqhGkA358raT6D910OTjCGwtWOCz41vn/dQUlWv5KtL/6CsHKnJj4y4TszzgmxD0DsB5OjTvk3EYlQapVB4J4PvOaJ2yJVxRxQjr/dO653NeKTy5kKwmTyphiGI2FLBVRJT2GdqIhibVOvxPEElZi3mqNT78lUD9S9iREGs/KY01lVC1RMwxzIbnsxfCM6WNwlU/jmxjdsApVQ9NHY8ewcbPC+XcW5GOfecR0oHfxv1Jeexwpi58R9bn9ZQY0CuEImslHdFpcewkSJUbRDk5VLphPXs33Xj7qPFqMagOoE01lmrtkvurLizkrEU9koDQvrgqtsPg4ze6WGn/L7kf13/T4hNBuba+GYm2zo/0JXTHTNJRRTHQFrho+ivAERzfTyrHgtk8DOtozAoRtPQgoJrYiBGlYkFMgwAT1ZjQhaIH9cJXYI2lP+CekuJ3U+vlj/AAr1cWjSyyA+MnP7qf0bXBOZQ1KWmR1GfmKmM87po5lG3KnwbSl3oF9ZPBwcouokQZUW8clTkKJmgxkMJ7eUSXq9nDudaF4u0ULa88ZmoYMjaYHkU9pd/OZyqDVjlrqiiwYh+Y9pFmfA/YBZnw5+lgIVefyLUtw8m5v/KWwELOJ6WeqnQwFYHe9wkn/TgKqoONMd45+qaWpktZCqHWXvKvwbPktF1KENajZzleIz8N31LlHimtBtnxXNUEcnnDpETz/QMh6rHTiOxSwjeXXYdG0y5PZUg+kh62Go0T1X6OPIBWrLCTlW73KkObvjSDGEB/JItTjQU0yEt1hAFKOYD0sNtzikPWSO17UI0iKtgI6VtR0rlcWVcfUhouGkHuawuk41bNO9synlUNoEDoK2aZrQ9eatzIDOzOqn1AoEAqVS9f7TQCoJ7wECnoP87FQ9GPhdW8GMkcQGDTRX5yhAPrCxhAKCVDixZLf9fuQydpbzhozngBTDQH2NrS9pVLMp3f7hpTFSbQYMpxGjwsHQi+CvLdvZXPv0RNtze/hsr4D+bK4+EPTguDoh4hTmaZdv+IaeOWDTpupkIXXe6H/q5iylQ8yyeg37+hTyzZY9wRomu4j2//d1CDYtP0kLLmys5tmHq5/vmFi2a5FzNh9LenrQmHUcSwWFdVSU57JrhxBqhlyyxbBWYzHRzlQUToYBQA1zyzzl15yy8T/NIKDRGfGta5uR3vYO3u8X8hLU+Ga3Q1qfS7OHQMX1uKvkJ7gMa2znv14WllozpZaI9qlnmh1gkFnxNiAwcQNh8YzuTvBwiVOof5iw2Tg1Jk7/+tQWV/BjmJ2urG62CdbIdRfTzQPmNYCp42rxIC8R3fjEWvfXNJQ/llo2TiX56IcK1WhcPcNaOl9YDbKISkDgWOVcjA/5aW4QhcSF+5VufpjsIKKkUE4rYc/LfLyjYJrYLKPMuhd90KcfVlNWU2nwO7onV/tPzOyR98BDrS0Cw5WC63cnXvYJf5rMBEMF2zBa2IrMNqeE6I/6pY/yyafVibOXW6/+UT/A8UmPt2npP9/WSqu8ddEJlappvSc03DlBz+lShpDNhLNO7HGZr0imR9MvOIYPOpsaz+PjTU/xZAwrPdpbIca5nbGLRYcWx8DOTHx8ACl5rE7mg/0w7+7wavPwwFIZs/CQ1020hGOwWBBKXOkIT4JhRjY8zS3ulFtBA7jz2v7HSBF90zuJVryI0aogljKnYhWxUVa5ZqQ6M4rkLoGOQqIfpF/XKYiKmw0wlViOUlueThaE+X2msD308gPb9R4IeIpJAO4OV07fHI72NeAbGc2yWk8XthtTlMV7t4U2xahc+iaUkCBEaR+DclZKvookqrfllkhDyn67BauBn/6cPaOaTxpwv454vgiQWrZj9QAAA'
    # hm.set('image_data', IMAGE)
    hm.set('image', 'https://cdn.prod.website-files.com/6600c65ea72e48aee6a742fe/6609b080d3a32bb0fd1a0381_token.png')

    # begin_cell().store_uint(1, 8).store_snake_string('https://...').end_cell()

    return begin_cell().store_uint(0, 8).store_dict(hm.serialize()).end_cell()


async def get_minter(client: LiteBalancer):
    content = get_metadata()
    data = JettonMinterData(
        total_supply=0,
        admin_address=Address('UQCPCZU37-aComPLgaQBcOkevn4x5GJHSfZsFt6eF9DpHZH9'),
        content=content,
        jetton_wallet_code=jetton_wallet_code
    )
    state_init = StateInit(code=jetton_minter_code, data=data.serialize())
    return await Contract.from_state_init(client, workchain=0, state_init=state_init)


async def deploy_minter(client: LiteBalancer):
    wallet = await WalletV4R2.from_mnemonic(client, mnemo)
    minter = await get_minter(client)
    await wallet.transfer(destination=minter.address, amount=2*10**7, state_init=minter.state_init)


def get_mint_body(addr: str, ton_amount: int, token_amount: int):
    return (begin_cell()
            .store_uint(21, 32)
            .store_uint(0, 64)
            .store_address(addr)
            .store_coins(ton_amount)
            .store_ref(
                begin_cell()
                .store_uint(0x178d4519, 32)
                .store_uint(0, 64)
                .store_coins(token_amount)
                .store_address(None)
                .store_address(None)
                .store_coins(0)
                .store_bit(0)
                .end_cell()
            )
            .end_cell())


def get_change_owner_body(new_owner: Address):
    return (begin_cell()
            .store_uint(3, 32)
            .store_uint(0, 64)
            .store_address(new_owner)
            .end_cell())


async def mint_tokens(client: LiteBalancer):
    body = get_mint_body('UQCPCZU37-aComPLgaQBcOkevn4x5GJHSfZsFt6eF9DpHZH9', 2*10**7, token_amount=10000*10**9)
    wallet = await WalletV4R2.from_mnemonic(client, mnemo)
    minter = await get_minter(client)
    await wallet.transfer(destination=minter.address, amount=4*10**7, body=body)


async def change_owner(client: LiteBalancer):
    body = get_change_owner_body(Address((0, b'\x00' * 32)))
    wallet = await WalletV4R2.from_mnemonic(client, mnemo)
    minter = await get_minter(client)
    await wallet.transfer(destination=minter.address, amount=2*10**7, body=body)


async def main():
    async with LiteBalancer.from_mainnet_config(trust_level=2) as client:
        # await deploy_minter(client)
        # await mint_tokens(client)
        await change_owner(client)

asyncio.run(main())