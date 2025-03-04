#include <boost/ut.hpp>
#include <spdlog/spdlog.h>
#include <string>

#include <gnuradio-4.0/Scheduler.hpp>
#include <gnuradio-4.0/soapy/Soapy.hpp>
#include <gnuradio-4.0/zeromq/Zmq.hpp>
#include <gnuradio-4.0/testing/NullSources.hpp>

// Define a constant buffer size
const std::size_t BUFFER_SIZE = 2048;

gr::Graph createGraph(std::string zmqPubAddr1, std::string zmqPubAddr2, float sampleRate, double rxCenterFrequency, double bandwidth, double rxGains) {
    using namespace boost::ut;
    using namespace gr;
    using namespace gr::blocks::soapy;
    using namespace gr::blocks::zeromq;

    Graph flow;
    using TDataType = std::complex<float>;

    // Create source block with specified buffer size
    auto& source = flow.emplaceBlock<SoapyBlock<TDataType, 2UZ>>({
        {"device", "lime"},                                                                 //
        {"sample_rate", sampleRate},                                                        //
        {"rx_channels", std::vector<gr::Size_t>{0U, 1U}},                                   //
        {"rx_antennae", std::vector<std::string>{"LNAW", "LNAW"}},                          //
        {"rx_center_frequency", std::vector<double>{rxCenterFrequency, rxCenterFrequency}}, //
        {"rx_bandwidth", std::vector<double>{bandwidth, bandwidth}},                        //
        {"rx_gains", std::vector<double>{rxGains, rxGains}},                                //
        {"buffer_size", BUFFER_SIZE}                                                        // Specify buffer size
    });
    spdlog::info("set parameter: sample_rate: {} SP/s, rx_center_frequency: {} Hz, rx_bandwidth: {} Hz, rx_gains: {} dB", //
                 sampleRate, rxCenterFrequency, bandwidth, rxGains);

    if (zmqPubAddr1.contains("null")) {
        spdlog::info("write channel0 to NullSink");
        auto& zmqSink1 = flow.emplaceBlock<testing::NullSink<TDataType>>();
        zmqSink1.set_output_multiple(BUFFER_SIZE); // Set buffer size for NullSink
        expect(eq(gr::ConnectionResult::SUCCESS, flow.connect<"out0">(source).to<"in">(zmqSink1))) << "error connecting NullSink1";
    } else {
        spdlog::info("write to ZMQ PUB address: {}", zmqPubAddr1);
        auto& zmqSink1 = flow.emplaceBlock<ZmqPubSink<TDataType>>({
            {"addr", zmqPubAddr1}, 
            {"buffer_size", BUFFER_SIZE} // Specify buffer size for ZMQ sink
        });
        expect(eq(gr::ConnectionResult::SUCCESS, flow.connect<"out0">(source).to<"in">(zmqSink1))) << "error connecting ZmqPubSink1";
    }

    if (zmqPubAddr2.contains("null")) {
        spdlog::info("write channel1 to NullSink");
        auto& zmqSink2 = flow.emplaceBlock<testing::NullSink<TDataType>>();
        zmqSink2.set_output_multiple(BUFFER_SIZE); // Set buffer size for NullSink
        expect(eq(gr::ConnectionResult::SUCCESS, flow.connect<"out1">(source).to<"in">(zmqSink2))) << "error connecting NullSink2";
    } else {
        spdlog::info("write to ZMQ PUB address: {}", zmqPubAddr2);
        auto& zmqSink2 = flow.emplaceBlock<ZmqPubSink<TDataType>>({
            {"addr", zmqPubAddr2}, 
            {"buffer_size", BUFFER_SIZE} // Specify buffer size for ZMQ sink
        });
        expect(eq(gr::ConnectionResult::SUCCESS, flow.connect<"out1">(source).to<"in">(zmqSink2))) << "error connecting ZmqPubSink2";
    }

    return flow;
}

int main(int argc, char* argv[]) {
    spdlog::info("Starting the acquisition...");

    try {
        using namespace boost::ut;
        using namespace gr;
        using namespace gr::blocks::soapy;
        using namespace gr::blocks::zeromq;

        std::string zmqPubAddr1 = "tcp://127.0.0.1:5555";
        std::string zmqPubAddr2 = "tcp://127.0.0.1:5556";
        float sampleRate = 1e6;
        double rxCenterFrequency = 2.4e9;
        double bandwidth = 1e6;
        double rxGains = 50.0;

        auto graph = createGraph(zmqPubAddr1, zmqPubAddr2, sampleRate, rxCenterFrequency, bandwidth, rxGains);

        gr::Scheduler scheduler;
        scheduler.run(graph);

        spdlog::info("Acquisition finished successfully.");
    } catch (const std::exception& e) {
        spdlog::error("An error occurred: {}", e.what());
        return 1;
    }

    return 0;
}
