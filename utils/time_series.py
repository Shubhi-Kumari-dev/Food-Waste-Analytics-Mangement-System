"""
Time Series Analysis Module for Food Waste Analytics and Management System.
Implements:
1. Temporal Aggregations (Daily, Weekly, Monthly)
2. Moving Averages
3. Exponential Smoothing (Statsmodels)
4. Classical Seasonal Decomposition (Trend, Seasonal, Residual)
5. ARIMA Forecasting with historical and forecasted projections
Includes robust safety checks and clear educational error handling.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
import warnings

warnings.filterwarnings('ignore')

def prepare_time_series(df, freq='D'):
    """
    Aggregates food waste by date and resamples to a regular frequency.
    freq: 'D' for daily, 'W' for weekly, 'ME' (or 'M') for monthly.
    Fills any missing dates in the interval with 0 or forward fill.
    Returns: pandas Series indexed by DatetimeIndex, with clean name 'Food_Wasted_Kg'.
    """
    if df is None or df.empty or 'Date' not in df.columns or 'Food_Wasted_Kg' not in df.columns:
        return None, "Dataset must contain valid 'Date' and 'Food_Wasted_Kg' columns."

    try:
        data = df.copy()
        data['Date'] = pd.to_datetime(data['Date'])
        # Group by date sum
        daily = data.groupby('Date')['Food_Wasted_Kg'].sum().sort_index()

        # Resample to ensure continuous date index
        resampled = daily.resample(freq).sum().fillna(0.0)

        if len(resampled) < 5:
            return None, "Insufficient data points across the selected time horizon (fewer than 5 periods)."

        return resampled, None
    except Exception as e:
        return None, f"Error preparing time series: {str(e)}"

def plot_trend_and_moving_average(ts_series, window_size=7, freq_label="Daily", theme_mode="light"):
    """
    Calculates moving average and plots both the original series and the moving average
    using Plotly with warm culinary styling.
    """
    ma_series = ts_series.rolling(window=window_size, min_periods=1).mean()
    is_dark = (theme_mode == "dark")
    text_color = '#FDF5ED' if is_dark else '#2A1B10'
    sub_color = '#BFAFA2' if is_dark else '#6B5746'
    grid_color = 'rgba(255, 235, 215, 0.08)' if is_dark else '#EFE4D6'

    fig = go.Figure()
    
    # Original series
    fig.add_trace(go.Scatter(
        x=ts_series.index,
        y=ts_series.values,
        mode='lines+markers',
        name=f'Actual Waste ({freq_label})',
        line=dict(color='#EA580C', width=2),
        marker=dict(size=4)
    ))

    # Moving Average
    fig.add_trace(go.Scatter(
        x=ma_series.index,
        y=ma_series.values,
        mode='lines',
        name=f'{window_size}-Period Moving Average',
        line=dict(color='#D97706', width=3, dash='solid')
    ))

    fig.update_layout(
        title=dict(text=""),
        font={'family': 'Plus Jakarta Sans, -apple-system, sans-serif', 'color': sub_color},
        xaxis_title="Date",
        yaxis_title="Total Waste (kg)",
        hovermode="x unified",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=35, r=25, t=15, b=55),
        legend=dict(orientation="h", yanchor="top", y=-0.16, xanchor="center", x=0.5, font=dict(color=sub_color))
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=grid_color, tickfont=dict(color=sub_color))
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=grid_color, tickfont=dict(color=sub_color))

    return fig, ma_series

def compute_exponential_smoothing(ts_series, alpha=0.3, theme_mode="light"):
    """
    Applies Simple Exponential Smoothing using Statsmodels.
    Formula: S_t = alpha * Y_t + (1 - alpha) * S_{t-1}
    Returns: (fig, smoothed_series, error_message)
    """
    try:
        model = SimpleExpSmoothing(ts_series, initialization_method="estimated")
        fit = model.fit(smoothing_level=alpha, optimized=False)
        smoothed = fit.fittedvalues

        is_dark = (theme_mode == "dark")
        text_color = '#FDF5ED' if is_dark else '#2A1B10'
        sub_color = '#BFAFA2' if is_dark else '#6B5746'
        grid_color = 'rgba(255, 235, 215, 0.08)' if is_dark else '#EFE4D6'

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=ts_series.index,
            y=ts_series.values,
            mode='lines+markers',
            name='Actual Food Waste',
            line=dict(color='#9CA3AF' if not is_dark else '#6B7280', width=1.5),
            marker=dict(size=3)
        ))
        fig.add_trace(go.Scatter(
            x=smoothed.index,
            y=smoothed.values,
            mode='lines',
            name=f'Exponentially Smoothed (α = {alpha})',
            line=dict(color='#16A34A', width=2.5)
        ))

        fig.update_layout(
            title=dict(text=""),
            font={'family': 'Plus Jakarta Sans, -apple-system, sans-serif', 'color': sub_color},
            xaxis_title="Date",
            yaxis_title="Food Waste (kg)",
            hovermode="x unified",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=35, r=25, t=15, b=55),
            legend=dict(orientation="h", yanchor="top", y=-0.16, xanchor="center", x=0.5, font=dict(color=sub_color))
        )
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=grid_color, tickfont=dict(color=sub_color))
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=grid_color, tickfont=dict(color=sub_color))
        return fig, smoothed, None
    except Exception as e:
        return None, None, f"Exponential smoothing failed: {str(e)}"

def compute_seasonal_decomposition(ts_series, period=7, model='additive', theme_mode="light"):
    """
    Performs classical time series decomposition (Observed = Trend + Seasonal + Residual).
    Requires at least 2 * period data points.
    Returns: (fig, decomp_result, error_message)
    """
    if len(ts_series) < 2 * period:
        return None, None, (
            f"Decomposition requires at least 2 full seasonal cycles. "
            f"You selected period = {period}, which requires >= {2 * period} observations, "
            f"but this series only has {len(ts_series)} observations."
        )

    try:
        series_clean = ts_series.copy()
        if model == 'multiplicative':
            series_clean = series_clean.clip(lower=0.1)

        result = seasonal_decompose(series_clean, model=model, period=period)

        is_dark = (theme_mode == "dark")
        text_color = '#FDF5ED' if is_dark else '#2A1B10'
        sub_color = '#BFAFA2' if is_dark else '#6B5746'
        grid_color = 'rgba(255, 235, 215, 0.08)' if is_dark else '#EFE4D6'

        from plotly.subplots import make_subplots
        fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.06,
            subplot_titles=("Observed Food Waste (kg)", "Trend Component", "Seasonal Pattern", "Residuals (Noise)")
        )

        # 1. Observed (Saffron)
        fig.add_trace(go.Scatter(x=ts_series.index, y=result.observed, mode='lines', name='Observed', line=dict(color='#EA580C')), row=1, col=1)
        # 2. Trend (Roasted Crimson)
        fig.add_trace(go.Scatter(x=ts_series.index, y=result.trend, mode='lines', name='Trend', line=dict(color='#BE123C', width=2.5)), row=2, col=1)
        # 3. Seasonal (Fresh Basil Green)
        fig.add_trace(go.Scatter(x=ts_series.index, y=result.seasonal, mode='lines', name='Seasonal', line=dict(color='#16A34A', width=2)), row=3, col=1)
        # 4. Residual (Toasted Bread Cinnamon)
        fig.add_trace(go.Scatter(x=ts_series.index, y=result.resid, mode='markers', name='Residual', marker=dict(color='#B45309', size=4)), row=4, col=1)

        fig.update_layout(
            height=650,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'family': 'Plus Jakarta Sans, -apple-system, sans-serif', 'color': sub_color},
            title_text=f"<b>Time Series Decomposition ({model.capitalize()} Model, Period = {period})</b>"
        )
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=grid_color, tickfont=dict(color=sub_color))
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=grid_color, tickfont=dict(color=sub_color))

        return fig, result, None
    except Exception as e:
        return None, None, f"Seasonal decomposition could not be performed: {str(e)}"

def run_arima_forecast(ts_series, order=(1, 1, 1), forecast_steps=14, theme_mode="light"):
    """
    Fits an ARIMA(p, d, q) model and forecasts future food waste with culinary theme colors.
    Returns: (fig, forecast_df, error_message)
    """
    if len(ts_series) < 15:
        return None, None, "ARIMA forecasting requires at least 15 historical observations to produce reliable estimates."

    try:
        model = ARIMA(ts_series, order=order)
        fitted_model = model.fit()

        forecast_res = fitted_model.get_forecast(steps=forecast_steps)
        forecast_values = forecast_res.predicted_mean
        conf_int = forecast_res.conf_int()

        last_date = ts_series.index[-1]
        freq_inferred = pd.infer_freq(ts_series.index) or 'D'
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_steps, freq=freq_inferred)

        forecast_df = pd.DataFrame({
            'Forecast_Date': future_dates.strftime('%Y-%m-%d'),
            'Predicted_Waste_Kg': np.maximum(0, forecast_values.values).round(2),
            'Lower_Bound_95%': np.maximum(0, conf_int.iloc[:, 0].values).round(2),
            'Upper_Bound_95%': np.maximum(0, conf_int.iloc[:, 1].values).round(2)
        })

        is_dark = (theme_mode == "dark")
        text_color = '#FDF5ED' if is_dark else '#2A1B10'
        sub_color = '#BFAFA2' if is_dark else '#6B5746'
        grid_color = 'rgba(255, 235, 215, 0.08)' if is_dark else '#EFE4D6'

        fig = go.Figure()

        # Historical series (Saffron Terracotta)
        fig.add_trace(go.Scatter(
            x=ts_series.index,
            y=ts_series.values,
            mode='lines',
            name='Historical Waste',
            line=dict(color='#EA580C', width=2)
        ))

        # Forecast line (Honey Amber)
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=forecast_df['Predicted_Waste_Kg'],
            mode='lines+markers',
            name=f'ARIMA{order} Forecast ({forecast_steps} periods)',
            line=dict(color='#D97706', width=2.5, dash='dash'),
            marker=dict(size=6, symbol='diamond')
        ))

        # Confidence interval ribbon
        fig.add_trace(go.Scatter(
            x=list(future_dates) + list(future_dates[::-1]),
            y=list(forecast_df['Upper_Bound_95%']) + list(forecast_df['Lower_Bound_95%'][::-1]),
            fill='toself',
            fillcolor='rgba(217, 119, 6, 0.18)',
            line=dict(color='rgba(255,255,255,0)'),
            name='95% Confidence Interval',
            showlegend=True
        ))

        fig.update_layout(
            title=dict(text=""),
            font={'family': 'Plus Jakarta Sans, -apple-system, sans-serif', 'color': sub_color},
            xaxis_title="Date",
            yaxis_title="Food Waste (kg)",
            hovermode="x unified",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=35, r=25, t=15, b=55),
            legend=dict(orientation="h", yanchor="top", y=-0.16, xanchor="center", x=0.5, font=dict(color=sub_color))
        )
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=grid_color, tickfont=dict(color=sub_color))
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=grid_color, tickfont=dict(color=sub_color))

        return fig, forecast_df, None
    except Exception as e:
        return None, None, f"ARIMA modeling failed: {str(e)}. Try adjusting parameters (p,d,q)."
