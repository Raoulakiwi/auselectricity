#!/bin/bash

# Australian Electricity Market Dashboard - Service Management Script

SERVICES=("auselectricity-backend" "auselectricity-frontend")

show_help() {
    echo "Australian Electricity Market Dashboard - Service Manager"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start     - Start all services"
    echo "  stop      - Stop all services"
    echo "  restart   - Restart all services"
    echo "  status    - Show status of all services"
    echo "  logs      - Show logs for all services"
    echo "  enable    - Enable services for auto-startup"
    echo "  disable   - Disable services from auto-startup"
    echo "  install   - Install and configure services"
    echo "  uninstall - Remove services from system"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 status"
    echo "  $0 logs"
}

run_command() {
    local cmd=$1
    local service=$2
    
    case $cmd in
        "start")
            echo "🚀 Starting $service..."
            sudo systemctl start $service
            ;;
        "stop")
            echo "🛑 Stopping $service..."
            sudo systemctl stop $service
            ;;
        "restart")
            echo "🔄 Restarting $service..."
            sudo systemctl restart $service
            ;;
        "status")
            echo "📊 Status of $service:"
            sudo systemctl status $service --no-pager -l
            echo ""
            ;;
        "logs")
            echo "📋 Logs for $service (last 20 lines):"
            sudo journalctl -u $service -n 20 --no-pager
            echo ""
            ;;
        "enable")
            echo "⚡ Enabling $service for auto-startup..."
            sudo systemctl enable $service
            ;;
        "disable")
            echo "🔌 Disabling $service from auto-startup..."
            sudo systemctl disable $service
            ;;
    esac
}

run_all_services() {
    local cmd=$1
    
    for service in "${SERVICES[@]}"; do
        run_command $cmd $service
    done
}

case "${1:-}" in
    "start")
        run_all_services "start"
        echo "✅ All services started"
        ;;
    "stop")
        run_all_services "stop"
        echo "✅ All services stopped"
        ;;
    "restart")
        run_all_services "restart"
        echo "✅ All services restarted"
        ;;
    "status")
        run_all_services "status"
        ;;
    "logs")
        run_all_services "logs"
        ;;
    "enable")
        run_all_services "enable"
        echo "✅ All services enabled for auto-startup"
        ;;
    "disable")
        run_all_services "disable"
        echo "✅ All services disabled from auto-startup"
        ;;
    "install")
        echo "🔧 Installing services..."
        chmod +x install_services.sh
        ./install_services.sh
        ;;
    "uninstall")
        echo "🗑️ Uninstalling services..."
        for service in "${SERVICES[@]}"; do
            echo "Stopping and disabling $service..."
            sudo systemctl stop $service 2>/dev/null || true
            sudo systemctl disable $service 2>/dev/null || true
        done
        sudo rm -f /etc/systemd/system/auselectricity-*.service
        sudo systemctl daemon-reload
        echo "✅ Services uninstalled"
        ;;
    "help"|"-h"|"--help"|"")
        show_help
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac


