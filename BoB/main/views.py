from django.shortcuts import render
import pandas as pd
import numpy as np
import csv
# Create your views here.


def home(requests):
    return render(requests, "index.html")


def evaluate(requests):
    if requests.method == "POST":
        data = requests.FILES.get("data")
        # Business growth Projection
        bgp = 1.05
        bgp = float(requests.POST.get("bgp"))
        print(bgp)

        # Replenishment horizon (days)
        rh = 2
        rh = float(requests.POST.get("rh"))

        # Default probability
        dp = 0.05
        dp = float(requests.POST.get("dp"))

        chest = requests.POST.get("chest")

        # notes
        twok = float(requests.POST.get("twok"))
        fiveh = float(requests.POST.get("fiveh"))
        twoh = float(requests.POST.get("twoh"))
        oneh = float(requests.POST.get("oneh"))
        fifty = float(requests.POST.get("fifty"))
        twenty = float(requests.POST.get("twenty"))
        ten = float(requests.POST.get("ten"))

        print(twok, fiveh, twoh, oneh, fifty, twenty, ten)

        data = pd.read_csv(data)
        data = data[['Transaction Date', 'Withdrawal', 'Deposit']]
        data = data.rename(columns={
                           "Transaction Date": "date", "Withdrawal": "withdrawal", "Deposit": "deposit"})
        data.dropna(inplace=True)
        data['date'] = pd.to_datetime(data['date'], dayfirst=True)
        data = data.groupby('date').agg(
            {'withdrawal': 'sum', 'deposit': 'sum'}).reset_index()

        data['netChange'] = data['deposit'] - data['withdrawal']
        data['netChange'] = data['netChange']/10000000
        total_deposit = sum(data['deposit'])
        total_withdrawal = sum(data['withdrawal'])
        Net = total_deposit - total_withdrawal

        overall_mean = np.mean(data['netChange'])
        overall_std = np.std(data['netChange'])
        monthly_avg = data.groupby(pd.PeriodIndex(data['date'], freq="M"))[
            'netChange'].mean().reset_index()

        monthly_std = data.groupby(pd.PeriodIndex(data['date'], freq="M"))[
            'netChange'].std().reset_index()

        from scipy.stats import norm
        overall_rl = max(-norm.ppf(dp, bgp*rh*overall_mean,
                         (overall_std)*(bgp*rh)**0.5), 0)

        rl = -norm.ppf(dp, bgp*rh*monthly_avg['netChange'],
                       (monthly_std['netChange'])*(bgp*rh)**0.5)

        rl[rl < 0] = 0
        final_df = monthly_avg
        final_df['std'] = monthly_std['netChange']
        final_df = final_df.rename(columns={"netChange": "mean"})
        final_df['Reserve Level (Crores)'] = rl

        # 2000Rs
        final_df['mean_2000'] = final_df['mean']*(twok/100)
        final_df['std_2000'] = final_df['std']*(twok/100)
        rl_2000 = -norm.ppf(dp, bgp*rh*final_df['mean_2000'],
                            (final_df['std_2000'])*(bgp*rh)**0.5)
        rl_2000[rl_2000 < 0] = 0
        final_df['rl_2000'] = rl_2000
        overall_mean_2000 = np.mean(final_df['mean_2000'])
        overall_std_2000 = np.std(final_df['std_2000'])
        overall_rl_2000 = max(0, -norm.ppf(dp, bgp*rh*overall_mean_2000,
                                           (overall_std_2000)*(bgp*rh)**0.5))

        # 500Rs
        final_df['mean_500'] = final_df['mean']*(fiveh/100)
        final_df['std_500'] = final_df['std']*(fiveh/100)
        rl_500 = -norm.ppf(dp, bgp*rh*final_df['mean_500'],
                           (final_df['std_500'])*(bgp*rh)**0.5)
        rl_500[rl_500 < 0] = 0
        final_df['rl_500'] = rl_500
        overall_mean_500 = np.mean(final_df['mean_500'])
        overall_std_500 = np.std(final_df['std_500'])
        overall_rl_500 = max(0, -norm.ppf(dp, bgp*rh*overall_mean_500,
                                          (overall_std_500)*(bgp*rh)**0.5))

        # 200Rs
        final_df['mean_200'] = final_df['mean']*(twoh/100)
        final_df['std_200'] = final_df['std']*(twoh/100)
        rl_200 = -norm.ppf(dp, bgp*rh*final_df['mean_200'],
                           (final_df['std_200'])*(bgp*rh)**0.5)
        rl_200[rl_200 < 0] = 0
        final_df['rl_200'] = rl_200
        overall_mean_200 = np.mean(final_df['mean_200'])
        overall_std_200 = np.std(final_df['std_200'])
        overall_rl_200 = max(0, -norm.ppf(dp, bgp*rh*overall_mean_200,
                                          (overall_std_200)*(bgp*rh)**0.5))

        # 100Rs
        final_df['mean_100'] = final_df['mean']*(oneh/100)
        final_df['std_100'] = final_df['std']*(oneh/100)
        rl_100 = -norm.ppf(dp, bgp*rh*final_df['mean_100'],
                           (final_df['std_100'])*(bgp*rh)**0.5)
        rl_100[rl_100 < 0] = 0
        final_df['rl_100'] = rl_100
        overall_mean_100 = np.mean(final_df['mean_100'])
        overall_std_100 = np.std(final_df['std_100'])
        overall_rl_100 = max(0, -norm.ppf(dp, bgp*rh*overall_mean_100,
                                          (overall_std_100)*(bgp*rh)**0.5))

        # 50Rs
        final_df['mean_50'] = final_df['mean']*(fifty/100)
        final_df['std_50'] = final_df['std']*(fifty/100)
        rl_50 = -norm.ppf(dp, bgp*rh*final_df['mean_50'],
                          (final_df['std_50'])*(bgp*rh)**0.5)
        rl_50[rl_50 < 0] = 0
        final_df['rl_50'] = rl_50
        overall_mean_50 = np.mean(final_df['mean_50'])
        overall_std_50 = np.std(final_df['std_50'])
        overall_rl_50 = max(0, -norm.ppf(dp, bgp*rh*overall_mean_50,
                                         (overall_std_50)*(bgp*rh)**0.5))

        # 20Rs
        final_df['mean_20'] = final_df['mean']*(twenty/100)
        final_df['std_20'] = final_df['std']*(twenty/100)
        rl_20 = -norm.ppf(dp, bgp*rh*final_df['mean_20'],
                          (final_df['std_20'])*(bgp*rh)**0.5)
        rl_20[rl_20 < 0] = 0
        final_df['rl_20'] = rl_20
        overall_mean_20 = np.mean(final_df['mean_20'])
        overall_std_20 = np.std(final_df['std_20'])
        overall_rl_20 = max(0, -norm.ppf(dp, bgp*rh*overall_mean_20,
                                         (overall_std_20)*(bgp*rh)**0.5))

        # 10Rs
        final_df['mean_10'] = final_df['mean']*(ten/100)
        final_df['std_10'] = final_df['std']*(ten/100)
        rl_10 = -norm.ppf(dp, bgp*rh*final_df['mean_10'],
                          (final_df['std_10'])*(bgp*rh)**0.5)
        rl_10[rl_10 < 0] = 0
        final_df['rl_10'] = rl_10
        overall_mean_10 = np.mean(final_df['mean_10'])
        overall_std_10 = np.std(final_df['std_10'])
        overall_rl_10 = max(0, -norm.ppf(dp, bgp*rh*overall_mean_10,
                                         (overall_std_10)*(bgp*rh)**0.5))

        

        date = []
        final_df['date'][0].year
        final_df['date'][0].month
        month = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May',
                 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        for d in final_df['date']:
            date.append(f"{month[int(d.month)]}'{d.year}")

        rld = []
        for i in range(12):
            temp = []
            temp.append(date[i])
            temp.append(float("{:.2f}".format(rl_2000[i])))
            temp.append(float("{:.2f}".format(rl_500[i])))
            temp.append(float("{:.2f}".format(rl_200[i])))
            temp.append(float("{:.2f}".format(rl_100[i])))
            temp.append(float("{:.2f}".format(rl_50[i])))
            temp.append(float("{:.2f}".format(rl_20[i])))
            temp.append(float("{:.2f}".format(rl_10[i])))

            rld.append(temp)

        
        rl = []
        for v in final_df['Reserve Level (Crores)']:
            rl.append(float("{:.2f}".format(v)))

        mean = []
        for v in final_df['mean']:
            mean.append(float("{:.2f}".format(v)))

        std = []
        for v in final_df['std']:
            std.append(float("{:.2f}".format(v)))

    return render(requests, "index.html", {
        "overall_mean": "{:.2f}".format(overall_mean),
        "overall_std": "{:.2f}".format(overall_std),
        "overall_rl": "{:.2f}".format(overall_rl),
        "cl": (1-dp)*100,
        "chest": chest,
        'rl': rl[:12],
        'date': date,
        'mean': mean[:12],
        'std': std[:12],
        'total_deposit': total_deposit/10000000,
        'total_withdrawal': total_withdrawal/10000000,
        'net': Net/10000000,
        'twok': "{:.2f}".format(overall_rl_2000),
        'fiveh': "{:.2f}".format(overall_rl_500),
        'twoh': "{:.2f}".format(overall_rl_200),
        'oneh': "{:.2f}".format(overall_rl_100),
        "fifty": "{:.2f}".format(overall_rl_50),
        "twenty": "{:.2f}".format(overall_rl_20),
        "ten": "{:.2f}".format(overall_rl_10),
        "rld": rld
    })
