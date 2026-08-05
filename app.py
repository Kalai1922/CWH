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
    "VOLTAMP.NS","GPIL.NS","POLYCAB.NS","INGERRAND.NS","J&KBANK.NS","KTKBANK.NS","RPGLIFE.NS",
    "MSUMI.NS","NIITMTS.NS","CMSINFO.NS","TANLA.NS","GPPL.NS","PNB.NS","MARICO.NS",
    "SOUTHBANK.NS","DOMS.NS","EMAMILTD.NS","HCLTECH.NS","CELLO.NS","IEX.NS","ABSLAMC.NS",
    "TI.NS","GRAVITA.NS","UTIAMC.NS","JBCHEPHARM.NS","FORCEMOT.NS","HINDCOPPER.NS","PAGEIND.NS",
    "GROWW.NS","GRSE.NS","TRITURBINE.NS","GODFRYPHLP.NS","ENGINERSIN.NS","NATIONALUM.NS",
    "ZENTEC.NS","DABUR.NS","BLS.NS","NBCC.NS","SCHAEFFLER.NS","RATNAMANI.NS","LICI.NS",
    "CGPOWER.NS","CHAMBLFERT.NS","VESUVIUS.NS","ZFCVINDIA.NS","UNIONBANK.NS","ESABINDIA.NS",
    "GANESHHOU.NS","DBCORP.NS","SUZLON.NS","BAJFINANCE.NS","HEROMOTOCO.NS","BAYERCROP.NS",
    "CUB.NS","ANTHEM.NS","HAL.NS","CAPLIPOINT.NS","JWL.NS","SHARDAMOTR.NS","TIMKEN.NS",
    "MGL.NS","MARUTI.NS","OSWALPUMPS.NS","HYUNDAI.NS","HDFCAMC.NS","PGHH.NS","KIRLOSBROS.NS",
    "MAZDOCK.NS","SKFINDIA.NS","ITC.NS","SUNPHARMA.NS","BALUFORGE.NS","GVT&D.NS","INOXINDIA.NS",
    "ABB.NS","IMFA.NS","KFINTECH.NS","LOTUSDEV.NS","DIVISLAB.NS","KOTAKBANK.NS","CHOLAFIN.NS",
    "CUMMINSIND.NS","EICHERMOT.NS","OFSS.NS","COFORGE.NS","WELCORP.NS","KEI.NS","ACE.NS",
    "SUNTV.NS","BSOFT.NS","AJAXENGG.NS","ABBOTINDIA.NS","MPHASIS.NS","GILLETTE.NS",
    "PETRONET.NS","TDPOWERSYS.NS","PIDILITIND.NS","HINDUNILVR.NS","INDGN.NS","DODLA.NS",
    "AJANTPHARM.NS","KSB.NS","TCI.NS","COCHINSHIP.NS","KARURVYSYA.NS","IDBI.NS","LTIM.NS",
    "MAITHANALL.NS","NESCO.NS","MAHABANK.NS","CERA.NS","BANKINDIA.NS","ICICIGI.NS",
    "INDIANB.NS","IGIL.NS","GRINDWELL.NS","FIVESTAR.NS","CIGNITITEC.NS","MANAPPURAM.NS",
    "GLAXO.NS","APARINDS.NS","CAMS.NS","FIEMIND.NS","HSCL.NS","DRREDDY.NS","AXISBANK.NS",
    "CDSL.NS","SANOFICONR.NS","NMDC.NS","ELECON.NS","MCX.NS","PERSISTENT.NS","EIHOTEL.NS",
    "COROMANDEL.NS","ZENSARTECH.NS","BOSCHLTD.NS","ASIANPAINT.NS","UNITDSPR.NS","GABRIEL.NS",
    "DATAPATTNS.NS","SHAREINDIA.NS","BANKBARODA.NS","PRUDENT.NS","SURYAROSNI.NS","FINEORG.NS",
    "HDFCBANK.NS","TMB.NS","KPITTECH.NS","LTTS.NS","CONCORDBIO.NS","SHRIRAMFIN.NS","3MINDIA.NS",
    "HBLENGINE.NS","BSE.NS","MANINFRA.NS","IRCTC.NS","APLAPOLLO.NS","LTF.NS","NATCOPHARM.NS",
    "M&MFIN.NS","KSCL.NS","BEL.NS","ECLERX.NS","CRISIL.NS","TIINDIA.NS","SBIN.NS",
    "NESTLEIND.NS","WAAREEINDO.NS","SUNDARMFIN.NS","AKZOINDIA.NS","TCS.NS","LALPATHLAB.NS",
    "POLYMED.NS","SBICARD.NS","TATAELXSI.NS","TRAVELFOOD.NS","PACEDIGITK.NS","MUTHOOTFIN.NS",
    "COLPAL.NS","GHCL.NS","CIPLA.NS","SUMICHEM.NS","AVANTIFEED.NS","INFY.NS","BLUEJET.NS",
    "VBL.NS","COALINDIA.NS","PIIND.NS","SOLARINDS.NS","WAAREERTL.NS","ENRIN.NS","VINATIORGA.NS",
    "GARFIBRES.NS","HEXT.NS","SHRIPISTON.NS","BERGEPAINT.NS","CSBBANK.NS","CANBK.NS","CLEAN.NS",
    "ANANDRATHI.NS","RITES.NS","IGL.NS","CASTROLIND.NS","NEWGEN.NS","LGEINDIA.NS","TATATECH.NS",
    "PFIZER.NS","INDIAMART.NS","AWL.NS","AUBANK.NS","HAVELLS.NS","SUPREMEIND.NS","MSTCLTD.NS",
    "GRWRHITECH.NS","MARKSANS.NS","BANDHANBNK.NS","SPLPETRO.NS","FEDERALBNK.NS","TENNIND.NS",
    "RAILTEL.NS","VSTIND.NS","DHANUKA.NS","PGHL.NS","CENTRALBK.NS","IOB.NS","ALIVUS.NS",
    "NAM-INDIA.NS","JYOTHYLAB.NS","ICICIBANK.NS","ALKEM.NS"
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

option = st.selectbox("Select Stock Universe to Scan:", ["V40", "V40 Next", "V200", "Custom Tickers"])
if option == "V40":
    tickers = V40
elif option == "V40 Next":
    tickers = V40_NEXT
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
    trusting an Early Entry flag. Returns (True/False/None, note); None means unverifiable."""
    try:
        financials = stock.quarterly_financials
        profit_rows = [i for i in financials.index if 'Net Income' in i]
        if not profit_rows or financials.empty:
            return None, "no data — verify manually on Screener.in"
        series = financials.loc[profit_rows[0]].dropna()
        if len(series) < 2:
            return None, "insufficient data — verify manually on Screener.in"
        if series.nunique() <= 1:
            return None, "⚠️ data looks stale/duplicated (all quarters identical) — cannot verify, check Screener.in manually"
        latest = series.iloc[0]
        is_max = latest >= series.max()
        note = f"latest {latest:,.0f} vs best-of-{len(series)}-qtrs {series.max():,.0f} — VERIFY on Screener.in 5-10yr P&L, this window is short"
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
