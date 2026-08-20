import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide", page_title="CWH Scanner")

st.title("☕ Cup with Handle (CWH) Scanner")
st.write(
    "Finds a **U-shaped cup** (decline + recovery to near the prior high) followed by a "
    "**shallower handle** (smaller pullback near the top), then flags it as either:\n\n"
    "- **Confirmed Entry** — price has broken above the handle high (safe approach)\n"
    "- **Early Entry** — price is still forming the handle base and turning up, only shown for "
    "stocks with **highest-ever quarterly net profit** (aggressive approach, per Vivek sir's rule "
    "that pattern-only isn't enough conviction here)"
)

# ---------------- VSpartans Stock Universe ----------------
V40 = [
    "BAJAJHLDNG.NS","ABBOTINDIA.NS","AXISBANK.NS","PFIZER.NS","BERGEPAINT.NS","TITAN.NS",
    "HINDUNILVR.NS","BATAINDIA.NS","LT.NS","RELIANCE.NS","MARICO.NS","BAJAJ-AUTO.NS",
    "KOTAKBANK.NS","TCS.NS","DABUR.NS","SBIN.NS","VOLTAS.NS","PGHH.NS","ITC.NS",
    "BAJFINANCE.NS","ICICIBANK.NS","HCLTECH.NS","HDFCBANK.NS","HDFCLIFE.NS","GILLETTE.NS",
    "HAVELLS.NS","COLPAL.NS","PIDILITIND.NS","MARUTI.NS","HDFCAMC.NS","NESTLEIND.NS",
    "ICICIPRULI.NS","ICICIGI.NS","ASIANPAINT.NS","GLAXO.NS","DMART.NS","PAGEIND.NS",
    "INFY.NS","BAJAJFINSV.NS"
]

V40_NEXT = [
    "CDSL.NS","BSE.NS","JIOFIN.NS","ANGELONE.NS","CAMS.NS","MCX.NS","ULTRACEMCO.NS","ACC.NS",
    "TEAMLEASE.NS","ASTRAZEN.NS","CIPLA.NS","ERIS.NS","LALPATHLAB.NS","APOLLOHOSP.NS",
    "MEDANTA.NS","FORTIS.NS","ADANIPORTS.NS","JSWINFRA.NS","AWL.NS","GODREJCP.NS","DIXON.NS",
    "KAJARIACER.NS","HONAUT.NS","DMART.NS","RELAXO.NS","BLUESTARCO.NS","BOSCHLTD.NS",
    "EICHERMOT.NS","MRF.NS","M&M.NS","TATAMOTORS.NS","HYUNDAI.NS","INDHOTEL.NS","ITCHOTELS.NS",
    "UNITDSPR.NS","RADICO.NS","UBL.NS","VBL.NS"
]

V200 = [
    "LTM.NS",
    "PGHH.NS","WAAREEINDO.NS","TIPSMUSIC.NS","ICICIAMC.NS","COLPAL.NS","GILLETTE.NS","SANOFICONR.NS",
    "WAAREERTL.NS","NESTLEIND.NS","PGHL.NS","GVPIL.NS","GVT&D.NS","MCX.NS","IGIL.NS",
    "ENRIN.NS","ESABINDIA.NS","PAGEIND.NS","JPOLYINVST.NS","WEBELSOLAR.NS","TCS.NS","GLAXO.NS",
    "TENNIND.NS","CASTROLIND.NS","BSE.NS","HBLENGINE.NS","SANOFI.NS","ANANDRATHI.NS","INGERRAND.NS",
    "CRIZAC.NS","IEX.NS","3MINDIA.NS","CAMS.NS","MARICO.NS","IRCTC.NS","OFSS.NS",
    "ATLANTAELE.NS","EMMVEE.NS","ABBOTINDIA.NS","NAM-INDIA.NS","GRSE.NS","HDFCAMC.NS","HINDCOPPER.NS",
    "TRAVELFOOD.NS","DIXON.NS","GKENERGY.NS","CRAMC.NS","INFY.NS","GLENMARK.NS","NATIONALUM.NS",
    "CUMMINSIND.NS","ITC.NS","MSUMI.NS","WAAREEENER.NS","HYUNDAI.NS","OSWALPUMPS.NS","SOLARINDS.NS",
    "PRUDENT.NS","GROWW.NS","BEL.NS","FORCEMOT.NS","MAZDOCK.NS","SHARDAMOTR.NS","TRITURBINE.NS",
    "HEROMOTOCO.NS","SUZLON.NS","COALINDIA.NS","CHENNPETRO.NS","ECLERX.NS","AJANTPHARM.NS","PERSISTENT.NS",
    "TDPOWERSYS.NS","INOXINDIA.NS","POLYCAB.NS","BBTC.NS","CRISIL.NS","LGEINDIA.NS","ABSLAMC.NS",
    "CDSL.NS","HAL.NS","ACE.NS","APLAPOLLO.NS","ACUTAAS.NS","APARINDS.NS","PIDILITIND.NS",
    "DDEVPLSTIK.NS","NBCC.NS","ENGINERSIN.NS","VIKRAMSOLR.NS","EICHERMOT.NS","HCLTECH.NS","ANTHEM.NS",
    "KIRLPNU.NS","MSTCLTD.NS","GODFRYPHLP.NS","SHARDACROP.NS","HEXT.NS","TATAELXSI.NS","ABB.NS",
    "SKFINDIA.NS","LTIM.NS","POWERINDIA.NS","FIEMIND.NS","BLS.NS","KFINTECH.NS","BAYERCROP.NS",
    "JYOTHYLAB.NS","CPPLUS.NS","HINDUNILVR.NS","RUBICON.NS","VSTIND.NS","RRKABEL.NS","EMAMILTD.NS",
    "GPPL.NS","INDIAMART.NS","LALPATHLAB.NS","STYL.NS","SCHAEFFLER.NS","NMDC.NS","JAMNAAUTO.NS",
    "CGPOWER.NS","LTTS.NS","ASHOKA.NS","BLUEJET.NS","NEULANDLAB.NS","UNITDSPR.NS","ASIANPAINT.NS",
    "TANLA.NS","KPITTECH.NS","GABRIEL.NS","CHAMBLFERT.NS","SUPRIYA.NS","NEWGEN.NS","HAVELLS.NS",
    "KSB.NS","CAPLIPOINT.NS","AVANTIFEED.NS","DOMS.NS","RADICO.NS","PFIZER.NS","QUESS.NS",
    "AJAXENGG.NS","ALIVUS.NS","DHANUKA.NS","MANYAVAR.NS","VOLTAMP.NS","COFORGE.NS","SUMICHEM.NS",
    "KAJARIACER.NS","NSDL.BO","TECHM.NS","RAILTEL.NS","ZENSARTECH.NS","PETRONET.NS","JSWDULUX.NS",
    "BALUFORGE.NS","REFEX.NS","MISHTANN.BO","HSCL.NS","MPHASIS.NS","ELGIEQUIP.NS","COROMANDEL.NS",
    "RITES.NS","BIKAJI.NS","DIVISLAB.NS","DATAPATTNS.NS","ICICIGI.NS","BERGEPAINT.NS","BOSCHLTD.NS",
    "FINEORG.NS","SIEMENS.NS","VESUVIUS.NS","VINATIORGA.NS","WABAG.NS","BLUESTARCO.NS","ALKEM.NS",
    "GRINDWELL.NS","BSOFT.NS","LOTUSDEV.NS","AIAENG.NS","TATATECH.NS","ELECON.NS","SUPREMEIND.NS",
    "EIHOTEL.NS","CLEAN.NS","NIITMTS.NS","SUNPHARMA.NS","AHLUCONT.NS","GPIL.NS","KIRLOSBROS.NS",
    "DABUR.NS","KEI.NS",
    "BAJFINANCE.NS","MUTHOOTFIN.NS","SHRIRAMFIN.NS","CHOLAFIN.NS","SBICARD.NS","SUNDARMFIN.NS","FIVESTAR.NS",
]

def dedupe(tickers):
    seen, out = set(), []
    for t in tickers:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out

V40 = dedupe(V40)
V40_NEXT = dedupe(V40_NEXT)
V200 = dedupe(V200)

# ---------------- V50 (stricter V200 filter) ----------------
FINANCIALS_V50 = {
    "BAJFINANCE.NS", "MUTHOOTFIN.NS", "SHRIRAMFIN.NS", "CHOLAFIN.NS",
    "SBICARD.NS", "SUNDARMFIN.NS", "FIVESTAR.NS"
}

@st.cache_data(ttl=86400, show_spinner=False)
def compute_v50_universe(v200_list, financials_set):
    """Applies Vivek sir's stricter V50 filters on top of V200 (per V50of_v200 notes):
    non-financials need Debt/Equity<0.2, Net Profit>Rs.250cr, ROCE>25%, YoY qtr profit growth>0,
    price<0.75xATH. Financials (banks/NBFC) need ROE>15%, Net Profit>Rs.1500cr, price<0.75xATH.
    PSU/government companies are excluded per the V200 criteria doc unless manually overridden.
    NOTE: yfinance doesn't expose a true ROCE figure — this uses returnOnAssets as an imperfect
    proxy, so any pass here still needs a Screener.in cross-check before you act on it, same as
    the highest-ever-profit checks elsewhere in this app."""
    passed = []
    for symbol in v200_list:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="max")
            if hist.empty:
                continue
            ath = hist['High'].max()
            current_price = hist['Close'].iloc[-1]
            if ath <= 0 or current_price >= 0.75 * ath:
                continue

            info = stock.info
            net_income = info.get("netIncomeToCommon")
            if net_income is None:
                continue

            if symbol in financials_set:
                roe = info.get("returnOnEquity")
                if roe is not None and roe * 100 > 15 and net_income > 1500 * 1e7:
                    passed.append(symbol)
            else:
                debt_to_equity = info.get("debtToEquity")
                roce_proxy = info.get("returnOnAssets")
                if debt_to_equity is None or roce_proxy is None:
                    continue
                de_ratio = debt_to_equity / 100 if debt_to_equity > 5 else debt_to_equity
                if de_ratio < 0.2 and net_income > 250 * 1e7 and roce_proxy * 100 > 25:
                    passed.append(symbol)
        except Exception:
            continue
    return passed

option = st.selectbox("Select Stock Universe to Scan:", ["V40", "V40 Next", "V50", "V200", "Custom Tickers"])
if option == "V40":
    tickers = V40
elif option == "V40 Next":
    tickers = V40_NEXT
elif option == "V50":
    with st.spinner("Applying V50 filters to the V200 universe... this checks fundamentals for every stock, so it can take a minute."):
        tickers = compute_v50_universe(V200, FINANCIALS_V50)
    st.caption(f"V50 found {len(tickers)} stock(s) passing the stricter filter. Cross-check on Screener.in before acting — see note above.")
elif option == "V200":
    tickers = V200
else:
    symbols_input = st.text_input(
        "Enter Custom Tickers (comma separated)",
        "RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS"
    )
    tickers = [s.strip() for s in symbols_input.split(",") if s.strip()]

st.info(f"Loaded {len(tickers)} stocks for scanning.")

with st.sidebar:
    st.header("Tuning")
    pivot_window = st.slider("Pivot sensitivity (trading days)", 3, 10, 5)
    cup_depth_min = st.slider("Minimum cup depth (%)", 8.0, 25.0, 12.0, step=1.0)
    cup_depth_max = st.slider("Maximum cup depth (%)", 25.0, 60.0, 50.0, step=1.0)
    min_cup_days = st.slider("Minimum cup duration (trading days)", 10, 60, 20)
    max_cup_days = st.slider("Maximum cup duration (trading days)", 60, 400, 260)
    rim_tolerance = st.slider("Right rim tolerance vs left rim (%)", 3.0, 15.0, 10.0, step=1.0,
                               help="How far the recovery peak can differ from the original left-side peak and still count as a matching rim.") / 100
    handle_max_depth = st.slider("Maximum handle depth (%)", 5.0, 20.0, 15.0, step=1.0) / 100
    max_handle_days = st.slider("Maximum handle duration (trading days)", 5, 40, 25)
    breakout_buffer = st.slider("Confirmed breakout buffer above handle high (%)", 0.0, 3.0, 0.5, step=0.5) / 100

def find_pivots(df, window):
    highs = df['High'].values
    lows = df['Low'].values
    n = len(df)
    piv_high_idx, piv_low_idx = [], []
    for i in range(window, n - window):
        seg_h = highs[i-window:i+window+1]
        seg_l = lows[i-window:i+window+1]
        if highs[i] == seg_h.max():
            piv_high_idx.append(i)
        if lows[i] == seg_l.min():
            piv_low_idx.append(i)
    return piv_high_idx, piv_low_idx

def detect_cwh(df, piv_high_idx):
    """Search for the most recent valid cup+handle. Returns a dict or None."""
    highs, lows, closes = df['High'].values, df['Low'].values, df['Close'].values
    n = len(df)

    for a_idx in sorted(piv_high_idx, reverse=True):
        left_rim = highs[a_idx]
        search_end = min(n - 1, a_idx + max_cup_days)
        if search_end - a_idx < min_cup_days:
            continue

        # Cup bottom: lowest low after the left rim, within the duration window
        window_lows = lows[a_idx+1:search_end+1]
        if len(window_lows) == 0:
            continue
        b_offset = window_lows.argmin()
        b_idx = a_idx + 1 + b_offset
        cup_bottom = lows[b_idx]
        if cup_bottom <= 0:
            continue
        cup_depth = (left_rim - cup_bottom) / left_rim * 100
        if not (cup_depth_min <= cup_depth <= cup_depth_max):
            continue

        # Right rim: highest high after the cup bottom, within the same duration window
        window_highs = highs[b_idx+1:search_end+1]
        if len(window_highs) == 0:
            continue
        c_offset = window_highs.argmax()
        c_idx = b_idx + 1 + c_offset
        right_rim = highs[c_idx]
        if abs(right_rim - left_rim) / left_rim > rim_tolerance:
            continue
        if (c_idx - a_idx) < min_cup_days:
            continue
        if c_idx >= n - 1:
            continue  # no bars left to form a handle

        # Handle: lowest low after the right rim, within handle duration window
        handle_end = min(n - 1, c_idx + max_handle_days)
        window_handle_lows = lows[c_idx+1:handle_end+1]
        if len(window_handle_lows) == 0:
            continue
        d_offset = window_handle_lows.argmin()
        d_idx = c_idx + 1 + d_offset
        handle_low = lows[d_idx]
        handle_depth = (right_rim - handle_low) / right_rim
        if handle_depth > handle_max_depth or handle_depth > (cup_depth / 100) * 0.5:
            continue

        return {
            "left_rim_idx": a_idx, "left_rim": left_rim,
            "cup_bottom_idx": b_idx, "cup_bottom": cup_bottom, "cup_depth_pct": cup_depth,
            "right_rim_idx": c_idx, "right_rim": right_rim,
            "handle_low_idx": d_idx, "handle_low": handle_low, "handle_depth_pct": handle_depth * 100,
        }
    return None

def reversal_confirmed(df):
    if len(df) < 3:
        return False
    last3 = df.iloc[-3:]
    return last3['High'].values[-1] > last3['High'].values[-2] and last3['Low'].values[-1] > last3['Low'].values[-2]

def is_highest_ever_profit(stock):
    """Approximate check using yfinance quarterly financials (typically last 4-5 quarters only).
    IMPORTANT: this is a shallow window — always verify against Screener.in's 5-10yr P&L before
    trusting an Early Entry flag. Returns (True/False/None, note); None means unverifiable.
    Shows the FULL quarterly series so a genuine new-high pass (latest ties the max because it
    IS the max) can be told apart from stale/duplicated data (every quarter shows the same number)."""
    try:
        financials = stock.quarterly_financials
        profit_rows = [i for i in financials.index if 'Net Income' in i]
        if not profit_rows or financials.empty:
            return None, "no data — verify manually on Screener.in"
        series = financials.loc[profit_rows[0]].dropna()
        if len(series) < 2:
            return None, "insufficient data — verify manually on Screener.in"
        values_str = ", ".join(f"{v:,.0f}" for v in series.values)
        if series.nunique() <= 1:
            return None, f"⚠️ ALL quarters identical ({values_str}) — this is stale/duplicated data, not a real flat profit run. Verify on Screener.in manually."
        latest = series.iloc[0]
        is_max = latest >= series.max()
        note = f"quarters (latest→oldest): {values_str} — {'latest IS the highest' if is_max else 'latest is NOT the highest'}. Always confirm on Screener.in 5-10yr P&L, this window is short."
        return is_max, note
    except Exception:
        return None, "error fetching — verify manually on Screener.in"

if st.button("Run CWH Scan"):
    results = []
    progress = st.progress(0, text="Starting scan...")

    for n_done, symbol in enumerate(tickers, start=1):
        progress.progress(n_done / len(tickers), text=f"Scanning {symbol}...")
        try:
            stock = yf.Ticker(symbol)
            df = stock.history(period="2y")
            if df.empty or len(df) < min_cup_days + 20:
                continue
            df = df.reset_index()

            piv_high_idx, _ = find_pivots(df, pivot_window)
            pattern = detect_cwh(df, piv_high_idx)
            if pattern is None:
                continue

            current_price = df['Close'].iloc[-1]
            handle_high = pattern["right_rim"]
            handle_low = pattern["handle_low"]

            is_confirmed = current_price > handle_high * (1 + breakout_buffer)
            is_early_candidate = (
                handle_low <= current_price <= handle_high
                and reversal_confirmed(df)
            )

            entry_type = None
            fund_note = ""
            if is_confirmed:
                entry_type = "Confirmed Entry"
            elif is_early_candidate:
                improving, note = is_highest_ever_profit(stock)
                if improving:
                    entry_type = "Early Entry"
                    fund_note = note
                else:
                    continue  # early entry requires the fundamental conviction check
            else:
                continue

            cup_target = handle_high + (pattern["left_rim"] - pattern["cup_bottom"])
            target_upside = ((cup_target - current_price) / current_price) * 100

            results.append({
                "Symbol": symbol,
                "Entry Type": entry_type,
                "Current Price": f"₹{current_price:.2f}",
                "Left Rim": round(pattern["left_rim"], 2),
                "Cup Bottom": round(pattern["cup_bottom"], 2),
                "Cup Depth": f"{pattern['cup_depth_pct']:.1f}%",
                "Right Rim / Handle High": round(handle_high, 2),
                "Handle Low": round(handle_low, 2),
                "Handle Depth": f"{pattern['handle_depth_pct']:.1f}%",
                "Fundamental Check": fund_note if fund_note else "—",
                "Target (Cup Depth Added)": round(cup_target, 2),
                "Target Upside": f"{target_upside:.1f}%"
            })
        except Exception:
            continue

    progress.empty()

    if results:
        res_df = pd.DataFrame(results)
        st.success(f"Found {len(res_df)} stock(s) matching a Cup with Handle setup.")
        st.dataframe(res_df, use_container_width=True)
    else:
        st.info(
            "No stocks currently show a valid cup + handle with a live entry trigger. "
            "This pattern is inherently rare and multi-week to form — an empty result "
            "most days is expected, not a bug."
        )

