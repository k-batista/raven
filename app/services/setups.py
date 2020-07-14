
from app.dataclass.setup_dataclass import SetupFactory

setup_factory = SetupFactory()

setup_factory.add('Possível Setup 9.1 de Compra',
                  """ stock_0_price_close >= stock_0_ema_9
                and stock_0_price_close > stock_0_price_open
                and stock_1_price_close <= stock_1_ema_9
                and stock_2_price_close <= stock_2_ema_9
                and stock_3_price_close <= stock_3_ema_9
                and stock_1_ema_9 < stock_2_ema_9
                and stock_2_ema_9 < stock_3_ema_9
                and stock_3_ema_9 < stock_4_ema_9
                """)

setup_factory.add('Possível PC de Compra',
                  """ stock_0_price_low <= stock_0_ema_21
                and (stock_0_price_close <= stock_1_price_close
                    or stock_0_price_close <= stock_1_price_open)
                and (stock_1_price_close <= stock_2_price_close
                    or stock_1_price_close <= stock_2_price_open)
                and (stock_0_price_close >= stock_0_ema_21
                    or stock_0_price_open >= stock_0_ema_21)
                and stock_1_price_close >= stock_0_ema_21
                and stock_2_price_close >= stock_0_ema_21
                and stock_3_price_close >= stock_0_ema_21
                and stock_4_price_close >= stock_0_ema_21
                and stock_5_price_close >= stock_0_ema_21
                """)

setup_factory.add('Possível Setup 9.3 de Compra',
                  """ stock_0_price_close < stock_1_price_close
                and stock_0_price_close < stock_2_price_close
                and stock_1_price_close < stock_2_price_close
                and stock_0_price_close >= stock_0_ema_9
                and stock_1_price_close >= stock_0_ema_9
                and stock_0_ema_9 >= stock_1_ema_9
                and stock_1_ema_9 >= stock_2_ema_9
                and stock_2_ema_9 >= stock_3_ema_9
                and stock_3_ema_9 >= stock_4_ema_9
                and stock_4_ema_9 >= stock_5_ema_9
                """)

setup_factory.add('Possível Setup 9.2 de Compra',
                  """ (stock_0_price_close < stock_1_price_close
                      or stock_0_price_close < stock_1_price_open)
                and stock_0_price_close < stock_0_price_open
                and stock_0_ema_9 > stock_1_ema_9
                and stock_1_ema_9 > stock_2_ema_9
                and stock_2_ema_9 > stock_3_ema_9
                and stock_3_ema_9 > stock_4_ema_9
                and stock_4_ema_9 > stock_5_ema_9
                """)

setup_factory.add('Possível Setup 9.1 de Venda',
                  """ stock_0_price_close < stock_0_ema_9
                and stock_0_price_close <= stock_0_price_open
                and stock_1_price_close >= stock_1_ema_9
                and stock_2_price_close >= stock_2_ema_9
                and stock_3_price_close >= stock_3_ema_9
                and stock_1_ema_9 >= stock_2_ema_9
                and stock_2_ema_9 >= stock_3_ema_9
                and stock_3_ema_9 >= stock_4_ema_9
                """)

setup_factory.add('Possível Setup 9.3 de Venda',
                  """ stock_0_price_close > stock_2_price_close
                and stock_1_price_close > stock_2_price_close
                and stock_0_price_close < stock_0_ema_9
                and stock_1_price_close < stock_0_ema_9
                and stock_0_ema_9 < stock_1_ema_9
                and stock_1_ema_9 < stock_2_ema_9
                and stock_2_ema_9 < stock_3_ema_9
                and stock_3_ema_9 < stock_4_ema_9
                and stock_4_ema_9 < stock_5_ema_9
                """)

setup_factory.add('Possível Setup 9.2 de Venda',
                  """ (stock_0_price_close > stock_1_price_close
                      or stock_0_price_close > stock_1_price_open)
                and stock_0_price_close > stock_0_price_open
                and stock_0_ema_9 < stock_1_ema_9
                and stock_1_ema_9 < stock_2_ema_9
                and stock_2_ema_9 < stock_3_ema_9
                and stock_3_ema_9 < stock_4_ema_9
                and stock_4_ema_9 < stock_5_ema_9
                """)

setup_factory.add('Possível PC de Venda',
                  """ stock_0_price_high > stock_0_ema_21
                and stock_0_price_close > stock_1_price_close
                and (stock_1_price_close > stock_2_price_close
                    or stock_1_price_close > stock_2_price_open)
                and (stock_2_price_close > stock_3_price_close
                    or stock_2_price_close > stock_3_price_open)
                and stock_0_price_open < stock_0_ema_21
                and stock_1_price_close < stock_0_ema_21
                and stock_2_price_close < stock_0_ema_21
                and stock_3_price_close < stock_0_ema_21
                and stock_4_price_close < stock_0_ema_21
                and stock_5_price_close < stock_0_ema_21
                """)
